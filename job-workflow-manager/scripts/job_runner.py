#!/usr/bin/env python3
"""
Job Workflow Runner CLI
Self-contained runner for Elton Boehnen's JobMaker BEJSON 104a Job System.
Handles job inspection, 1-task-at-a-time execution, plan/last contextualization,
auditing, template instantiation, and atomic state persistence.
"""

import sys
import os
import json
import re
import uuid
import argparse
from datetime import datetime
from pathlib import Path


def bejson_get_field_map(doc: dict) -> dict[str, int]:
    return {f["name"]: i for i, f in enumerate(doc.get("Fields", []))}


def bejson_atomic_write(file_path: str, doc: dict) -> bool:
    p = Path(file_path).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = p.parent / f".bejson_{os.getpid()}_{p.name}.tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        os.replace(tmp_path, p)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}", file=sys.stderr)
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        return False


def bejson_load_file(file_path: str) -> dict | None:
    p = Path(file_path)
    if not p.is_file():
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
        return None


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.strip()).strip("_").lower()
    return slug or "untitled_job"


def inspect_job(doc: dict, job_path: str):
    fmap = bejson_get_field_map(doc)
    goal = doc.get("Job_Goal", "")
    job_type = doc.get("Job_Type", "")
    job_subtype = doc.get("Job_Subtype", "")
    c_plan = bool(doc.get("Contextualize_Plan", False))
    c_last = bool(doc.get("Contextualize_Last", False))
    complete = bool(doc.get("Job_Complete", False))

    tasks = doc.get("Values", [])
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if len(t) > fmap.get("task_completed", 4) and t[fmap["task_completed"]])

    print("=" * 60)
    print(f"Job: {Path(job_path).stem}")
    print(f"Path: {job_path}")
    print(f"Goal: {goal}")
    if job_type or job_subtype:
        print(f"Type: {job_type} / {job_subtype}")
    print(f"Flags: Contextualize_Plan={c_plan} | Contextualize_Last={c_last}")
    print(f"Progress: {completed_tasks}/{total_tasks} completed | Job_Complete={complete}")
    print("-" * 60)

    for row in sorted(tasks, key=lambda r: r[fmap["task_order"]]):
        order = row[fmap["task_order"]]
        name = row[fmap["task_name"]]
        done = row[fmap["task_completed"]]
        mand = row[fmap["task_mandatory"]] if "task_mandatory" in fmap else False
        audit = row[fmap["audit_enabled"]]
        passed = row[fmap["audit_passed"]]
        status = "[DONE]" if done else "[PENDING]"
        if audit and not passed and not done:
            fail_r = row[fmap["audit_fail_reason"]]
            if fail_r:
                status = f"[AUDIT FAILED: {fail_r}]"
        badge = " (Mandatory)" if mand else ""
        print(f"  {order}. {status} {name}{badge}")
    print("=" * 60)


def step_next_task(doc: dict, job_path: str):
    fmap = bejson_get_field_map(doc)
    tasks = sorted(doc.get("Values", []), key=lambda r: r[fmap["task_order"]])

    active_idx = None
    prev_task = None
    for idx, row in enumerate(tasks):
        if not row[fmap["task_completed"]]:
            active_idx = idx
            break
        prev_task = row

    if active_idx is None:
        print("All tasks in this job are completed.")
        return

    active_row = tasks[active_idx]
    order = active_row[fmap["task_order"]]
    name = active_row[fmap["task_name"]]
    desc = active_row[fmap["task_description"]]
    audit_en = active_row[fmap["audit_enabled"]]
    mand = active_row[fmap["task_mandatory"]] if "task_mandatory" in fmap else False
    raw_ctx = active_row[fmap["task_context"]] if "task_context" in fmap else []
    raw_ref = active_row[fmap["task_reference"]] if "task_reference" in fmap else []

    print("\n" + "#" * 60)
    print(f"ACTIVE TASK TO EXECUTE: Task {order} of {len(tasks)}")
    print(f"Title: {name}")
    if mand:
        print("Note: Marked as MANDATORY step for this job type.")
    print("-" * 60)
    print(f"Description:\n{desc}\n")

    # 1. Contextualize Plan
    if doc.get("Contextualize_Plan"):
        print("--- [Contextualize Plan Injected] ---")
        print(f"Job Goal: {doc.get('Job_Goal')}")
        print("Full Task Schedule:")
        for t in tasks:
            t_ord = t[fmap["task_order"]]
            t_name = t[fmap["task_name"]]
            print(f"  - Step {t_ord}: {t_name}")
        print("--------------------------------------\n")

    # 2. Contextualize Last
    if doc.get("Contextualize_Last") and prev_task is not None:
        p_ord = prev_task[fmap["task_order"]]
        p_name = prev_task[fmap["task_name"]]
        p_desc = prev_task[fmap["task_description"]]
        print(f"--- [Contextualize Last Injected from Task {p_ord}] ---")
        print(f"Prior Task: {p_name}")
        print(f"Prior Description: {p_desc}")
        print("------------------------------------------------------\n")

    # 3. References
    if raw_ref:
        print(f"References ({len(raw_ref)} files):")
        for r in raw_ref:
            print(f"  - {r}")
        print()

    # 4. Embedded Context Chunks
    if raw_ctx:
        total_chunks = sum(len(c.get("chunks", [])) for c in raw_ctx if isinstance(c, dict))
        print(f"Embedded Context Chunks ({total_chunks} chunks across {len(raw_ctx)} files):")
        for c in raw_ctx:
            if isinstance(c, dict) and c.get("text_based"):
                print(f"  Source: {c.get('ref')} ({len(c.get('chunks', []))} chunks)")
        print()

    if audit_en:
        print("Audit Verification Required: Yes. Complete this task and verify before advancing.")
    print("#" * 60 + "\n")


def mark_task_complete(doc: dict, job_path: str, task_order: int, audit_passed: bool = True, audit_fail_reason: str = ""):
    fmap = bejson_get_field_map(doc)
    tasks = doc.get("Values", [])
    found = False

    for row in tasks:
        if row[fmap["task_order"]] == task_order:
            found = True
            if row[fmap["audit_enabled"]]:
                if audit_passed:
                    row[fmap["audit_passed"]] = True
                    row[fmap["audit_fail_reason"]] = ""
                    row[fmap["task_completed"]] = True
                else:
                    row[fmap["audit_passed"]] = False
                    row[fmap["audit_fail_reason"]] = audit_fail_reason or "Audit failed."
                    row[fmap["task_completed"]] = False
                    print(f"Task {task_order} marked as audit failed: {row[fmap['audit_fail_reason']]}")
            else:
                row[fmap["task_completed"]] = True
            break

    if not found:
        print(f"Error: Task {task_order} not found in {job_path}", file=sys.stderr)
        return False

    all_done = all(r[fmap["task_completed"]] for r in tasks)
    doc["Job_Complete"] = all_done
    if all_done:
        doc["Completion_Date"] = datetime.now().strftime("%Y-%m-%d")
        print(f"All tasks completed. Job '{Path(job_path).stem}' marked Job_Complete=true.")

    if bejson_atomic_write(job_path, doc):
        print(f"Successfully updated task {task_order} in {job_path}")
        return True
    return False


def instantiate_template(template_path: str, new_job_name: str, out_dir: str = "jobs") -> str | None:
    doc = bejson_load_file(template_path)
    if not doc:
        print(f"Error loading template: {template_path}", file=sys.stderr)
        return None

    fmap = bejson_get_field_map(doc)
    now = datetime.now().strftime("%Y-%m-%d")

    doc["Creation_Date"] = now
    doc["Completion_Date"] = ""
    doc["Job_Complete"] = False

    for row in doc.get("Values", []):
        row[fmap["task_id"]] = str(uuid.uuid4())
        row[fmap["task_completed"]] = False
        row[fmap["audit_passed"]] = False
        row[fmap["audit_fail_reason"]] = ""

    out_folder = Path(out_dir)
    out_folder.mkdir(parents=True, exist_ok=True)
    slug = slugify(new_job_name)
    target_path = out_folder / f"{slug}.bejson"

    if bejson_atomic_write(str(target_path), doc):
        print(f"Instantiated template into fresh Job Schema: {target_path}")
        return str(target_path)
    return None


def main():
    parser = argparse.ArgumentParser(description="Job Workflow Runner CLI")
    parser.add_argument("--inspect", metavar="JOB", help="Inspect job status and task list")
    parser.add_argument("--step", metavar="JOB", help="Show instructions and context for the next pending task")
    parser.add_argument("--complete", metavar="TASK_ORDER", type=int, help="Mark task order completed")
    parser.add_argument("--audit-fail", metavar="REASON", help="Mark task as audit failed with reason")
    parser.add_argument("--job", help="Target job file path for --complete actions")
    parser.add_argument("--instantiate", metavar="TEMPLATE", help="Instantiate template into fresh job")
    parser.add_argument("--name", help="Name for the newly instantiated job")

    args = parser.parse_args()

    if args.inspect:
        doc = bejson_load_file(args.inspect)
        if doc:
            inspect_job(doc, args.inspect)
    elif args.step:
        doc = bejson_load_file(args.step)
        if doc:
            step_next_task(doc, args.step)
    elif args.complete:
        if not args.job:
            print("Error: --job <path> required when using --complete", file=sys.stderr)
            sys.exit(1)
        doc = bejson_load_file(args.job)
        if doc:
            passed = args.audit_fail is None
            reason = args.audit_fail or ""
            mark_task_complete(doc, args.job, args.complete, passed, reason)
    elif args.instantiate:
        if not args.name:
            print("Error: --name <new_name> required when instantiating a template", file=sys.stderr)
            sys.exit(1)
        instantiate_template(args.instantiate, args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

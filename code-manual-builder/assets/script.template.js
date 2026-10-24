(function(){
  'use strict';
  var btn=document.getElementById('menuToggle'),
      closeBtn=document.getElementById('drawerClose'),
      drawer=document.getElementById('navDrawer'),
      backdrop=document.getElementById('drawerBackdrop'),
      search=document.getElementById('searchInput'),
      copyBtn=document.getElementById('copyCodeBtn'),
      catBtns=Array.prototype.slice.call(document.querySelectorAll('.nav-cat-btn'));
  function setDrawer(open){
    if(!drawer||!backdrop)return;
    drawer.classList.toggle('active',open);
    backdrop.classList.toggle('active',open);
    if(btn)btn.setAttribute('aria-expanded',open?'true':'false');
  }
  if(btn)btn.addEventListener('click',function(){setDrawer(!drawer.classList.contains('active'));});
  if(closeBtn)closeBtn.addEventListener('click',function(){setDrawer(false);});
  if(backdrop)backdrop.addEventListener('click',function(){setDrawer(false);});
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&drawer&&drawer.classList.contains('active'))setDrawer(false);
  });
  catBtns.forEach(function(b){
    b.addEventListener('click',function(){
      var parent=b.closest('.nav-cat');
      if(!parent)return;
      var isOpen=parent.classList.toggle('open');
      b.setAttribute('aria-expanded',isOpen?'true':'false');
    });
  });
  if(search){
    var cards=Array.prototype.slice.call(document.querySelectorAll('.module-card')),
        counter=document.getElementById('filterCount');
    search.addEventListener('input',function(){
      var q=(search.value||'').toLowerCase().trim(),shown=0;
      cards.forEach(function(c){
        var hay=(c.getAttribute('data-search')||'').toLowerCase();
        var match=!q||hay.indexOf(q)!==-1;
        c.style.display=match?'':'none';
        if(match)shown++;
      });
      if(counter)counter.textContent=shown+' / '+cards.length+' modules';
    });
  }
  if(copyBtn){
    copyBtn.addEventListener('click',function(){
      var codeEl=document.getElementById('sourceCodeBlock');
      if(!codeEl)return;
      var txt=codeEl.textContent||'';
      function done(){
        var orig=copyBtn.textContent;
        copyBtn.textContent='Copied';
        setTimeout(function(){copyBtn.textContent=orig;},1400);
      }
      if(navigator.clipboard&&navigator.clipboard.writeText){
        navigator.clipboard.writeText(txt).then(done).catch(function(){fallbackCopy(txt,done);});
      }else{
        fallbackCopy(txt,done);
      }
    });
  }
  function fallbackCopy(txt,cb){
    var ta=document.createElement('textarea');
    ta.value=txt;
    ta.style.position='fixed';
    ta.style.opacity='0';
    document.body.appendChild(ta);
    ta.select();
    try{document.execCommand('copy');cb();}catch(e){}
    document.body.removeChild(ta);
  }
})();

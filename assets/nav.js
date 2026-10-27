(function(){
  var nav=document.getElementById('site-nav'),btn=document.querySelector('.menu-toggle');
  if(btn&&nav){btn.addEventListener('click',function(){
    var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');});}
  document.querySelectorAll('.dropdown-toggle').forEach(function(t){
    t.addEventListener('click',function(){
      var li=t.parentNode,o=li.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){document.querySelectorAll('.has-dropdown.open').forEach(function(li){
      li.classList.remove('open');li.querySelector('.dropdown-toggle').setAttribute('aria-expanded','false');});}
  });
})();

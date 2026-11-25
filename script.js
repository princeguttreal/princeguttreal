const toggle=document.querySelector('.menu-toggle');const nav=document.querySelector('.nav');if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');}));}const year=document.querySelector('#year');if(year)year.textContent=new Date().getFullYear();
// Hide missing portfolio assets gracefully; cards retain their designed visual fallback.
document.querySelectorAll('.case-visual img').forEach((img)=>{img.addEventListener('error',()=>{img.hidden=true;},{once:true});});


// Fluid scroll reveals: one observer, staggered entrances and reduced-motion support.
const motionTargets=document.querySelectorAll('.section-kicker,.intro-grid>*,.services-head>*,.service-list article,.equipment-head>*,.equipment-grid>div,.portfolio-head>*,.case-card,.contact-layout>*');
const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reduceMotion&&'IntersectionObserver' in window){
  const revealObserver=new IntersectionObserver((entries,observer)=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target);}
    });
  },{threshold:.12,rootMargin:'0px 0px -45px 0px'});
  motionTargets.forEach((element,index)=>{
    element.classList.add('reveal');
    const group=element.parentElement;
    const siblings=[...group.children].filter(item=>item.matches('.reveal'));
    element.style.setProperty('--reveal-delay',(Math.min(siblings.length-1,4)*85)+'ms');
    revealObserver.observe(element);
  });
}else{
  motionTargets.forEach(element=>element.classList.add('is-visible'));
}

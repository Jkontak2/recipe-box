#!/usr/bin/env python3
"""Build a self-contained index.html recipe app from recipes.json.
Usage: python3 build.py   (writes index.html next to this file)"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
recipes = json.load(open(os.path.join(ROOT, "recipes.json"), encoding="utf-8"))
data = json.dumps(recipes, ensure_ascii=False).replace("</", "<\\/")

CATEGORIES = ["Breakfast","Lunch","Weeknight Dinner","Weekend Cooking","Chicken","Beef","Pork","Seafood","Pasta",
              "Soups & Stews","Grilling","Pizza","Sides","Appetizers","Desserts","Cocktails"]
used = [c for c in CATEGORIES if any(c in r["categories"] for r in recipes)]

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#b4472b">
<title>Joe's Recipe Box</title>
<style>
:root{--bg:#faf6f1;--card:#fff;--ink:#2b2622;--muted:#7a6f66;--accent:#b4472b;--accent2:#e9a23b;--line:#ece4da;--chip:#f2ebe3;--shadow:0 1px 2px rgba(60,40,20,.06),0 4px 14px rgba(60,40,20,.08);--r:16px}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
button{font:inherit;color:inherit;cursor:pointer}
a{color:var(--accent)}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
header.top{position:sticky;top:0;z-index:20;background:rgba(250,246,241,.94);backdrop-filter:saturate(1.4) blur(10px);-webkit-backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:baseline;justify-content:space-between;gap:8px;padding:12px 0 8px}
.filters{padding-top:10px;border-bottom:1px solid var(--line)}
.brand h1{margin:0;font-family:Georgia,"Times New Roman",serif;font-size:24px;letter-spacing:-.3px}
.brand h1 span{color:var(--accent)}
.brand .count{color:var(--muted);font-size:13px;white-space:nowrap}
.search{position:relative;margin-bottom:10px}
.search input{width:100%;border:1px solid var(--line);background:#fff;border-radius:12px;padding:11px 36px 11px 38px;font-size:16px;outline:none;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.search input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(180,71,43,.14)}
.search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);opacity:.5}
.search .clear{position:absolute;right:6px;top:50%;transform:translateY(-50%);border:0;background:none;font-size:20px;color:var(--muted);padding:4px 8px;display:none}
.seg{display:flex;background:var(--chip);border-radius:10px;padding:3px;margin-bottom:10px}
.seg button{flex:1;border:0;background:none;padding:7px 8px;border-radius:8px;font-weight:600;font-size:14px;color:var(--muted)}
.seg button.on{background:#fff;color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}
.chips{display:flex;gap:7px;overflow-x:auto;padding:0 0 10px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.chips::-webkit-scrollbar{display:none}
.chip{flex:0 0 auto;border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 12px;font-size:13px;font-weight:500;white-space:nowrap}
.chip.on{background:var(--ink);border-color:var(--ink);color:#fff}
.chip.quick{background:#fff7ec;border-color:#f3dcc0}
.chip.quick.on{background:var(--accent);border-color:var(--accent);color:#fff}
main{padding:6px 0 60px}
.status{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:13px;margin:6px 0 2px}
.status button{border:0;background:none;color:var(--accent);font-weight:600;padding:4px 0}
section.group{margin-top:18px}
section.group h2{display:flex;align-items:center;gap:8px;margin:0 0 10px;font-family:Georgia,serif;font-size:20px;letter-spacing:-.2px}
section.group h2 .n{font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--chip);color:var(--muted);border-radius:999px;padding:4px 8px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media(min-width:640px){.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
@media(min-width:960px){.grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
.card{display:flex;flex-direction:column;text-align:left;border:0;padding:0;background:var(--card);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow);transition:transform .15s ease,box-shadow .15s ease;min-width:0}
.card:active{transform:scale(.98)}
@media(hover:hover){.card:hover{transform:translateY(-2px);box-shadow:0 2px 4px rgba(60,40,20,.08),0 10px 24px rgba(60,40,20,.12)}}
.ph{position:relative;aspect-ratio:4/3;background:linear-gradient(135deg,#f3d9c4,#e9b48f);overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover;display:block}
.ph .noimg{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#7a3d22;font-family:Georgia,serif;font-size:30px;font-weight:700;gap:2px}
.ph .noimg small{font:600 10px/1 -apple-system,sans-serif;letter-spacing:.06em;text-transform:uppercase;opacity:.7}
.ph .time{position:absolute;left:8px;bottom:8px;background:rgba(20,14,10,.72);color:#fff;font-size:11.5px;font-weight:600;border-radius:999px;padding:3px 8px;display:flex;align-items:center;gap:4px}
.cb{padding:9px 10px 11px;display:flex;flex-direction:column;gap:3px;flex:1}
.cb h3{margin:0;font-size:14.5px;line-height:1.25;font-weight:650;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cb .by{color:var(--muted);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tags{display:flex;flex-wrap:nowrap;gap:4px;margin-top:auto;padding-top:5px;overflow:hidden}
.tags .tag{flex:0 1 auto;min-width:0}
.tag{font-size:10.5px;font-weight:600;background:var(--chip);color:#6b5d52;border-radius:6px;padding:2px 6px;white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis}
.tag.hot{background:#fdebd9;color:#9a4a12}
.empty{text-align:center;color:var(--muted);padding:60px 20px}
/* detail */
#detail{position:fixed;inset:0;z-index:50;background:var(--bg);overflow-y:auto;-webkit-overflow-scrolling:touch;display:none}
#detail.open{display:block;animation:up .22s ease}
@keyframes up{from{transform:translateY(24px);opacity:.4}to{transform:none;opacity:1}}
.d-hero{position:relative;aspect-ratio:4/3;max-height:52vh;width:100%;background:linear-gradient(135deg,#f3d9c4,#e9b48f);overflow:hidden}
.d-hero img{width:100%;height:100%;object-fit:cover;display:block}
.d-hero .noimg{font-size:56px}
.back{position:fixed;top:12px;left:12px;z-index:60;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.94);box-shadow:0 2px 10px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center}
.d-body{max-width:760px;margin:-26px auto 0;position:relative;background:var(--bg);border-radius:22px 22px 0 0;padding:20px 18px 110px}
.d-body h1{font-family:Georgia,serif;font-size:26px;line-height:1.15;margin:0 0 6px;letter-spacing:-.3px}
.credit{font-size:14px;color:var(--muted);margin-bottom:12px}
.credit b{color:var(--ink)}
.desc{margin:0 0 14px;font-size:15.5px}
.cta{display:flex;align-items:center;justify-content:center;gap:8px;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;font-size:16px;border-radius:14px;padding:14px 16px;box-shadow:0 6px 16px rgba(180,71,43,.28)}
.cta:active{transform:scale(.99)}
.sticky-cta{position:fixed;left:0;right:0;bottom:0;z-index:55;padding:10px 16px calc(10px + env(safe-area-inset-bottom));background:linear-gradient(to top,var(--bg) 70%,rgba(250,246,241,0));display:none}
#detail.open ~ .sticky-cta.show{display:block}
.sticky-cta .cta{max-width:728px;margin:0 auto}
.facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:14px 0 6px}
.fact{background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 9px;min-width:0}
.fact .k{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}
.fact .v{font-size:14px;font-weight:600;overflow-wrap:anywhere}
.d-sec{margin-top:22px}
.d-sec h2{font-family:Georgia,serif;font-size:19px;margin:0 0 10px;display:flex;justify-content:space-between;align-items:baseline}
.d-sec h2 small{font:500 12px -apple-system,sans-serif;color:var(--muted)}
ul.ing{list-style:none;margin:0;padding:0;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
ul.ing li{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-top:1px solid var(--line);font-size:14.5px}
ul.ing li:first-child{border-top:0}
ul.ing li .box{flex:0 0 18px;height:18px;border:2px solid #d8cbbd;border-radius:5px;margin-top:1px}
ul.ing li.done{color:#aaa;text-decoration:line-through}
ul.ing li.done .box{background:var(--accent);border-color:var(--accent)}
ol.steps{list-style:none;counter-reset:s;margin:0;padding:0}
ol.steps li{counter-increment:s;position:relative;padding:0 0 14px 40px;font-size:15px}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:-1px;width:28px;height:28px;border-radius:50%;background:var(--ink);color:#fff;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}
.note{background:#fff7ec;border:1px solid #f3dcc0;border-radius:14px;padding:12px 14px;font-size:14px}
.joe{background:#eef6ef;border:1px solid #cfe5d2}
.joe .row{display:flex;gap:14px;flex-wrap:wrap;font-size:14px}
.stars{color:var(--accent2);letter-spacing:1px}
.pill-row{display:flex;flex-wrap:wrap;gap:6px}
.src{font-size:12.5px;color:var(--muted);margin-top:18px;overflow-wrap:anywhere}
.unavail{background:#fdeeee;border:1px solid #f2c9c9;color:#8a2a2a;border-radius:12px;padding:10px 12px;font-size:14px}
body.lock{overflow:hidden}
</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <div class="brand"><h1>Joe's <span>Recipe Box</span></h1><div class="count" id="count"></div></div>
    <div class="search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Search name, ingredient, tag, creator…" autocomplete="off" aria-label="Search">
      <button class="clear" id="clear" aria-label="Clear search">×</button>
    </div>
  </div>
</header>
<div class="filters">
  <div class="wrap">
    <div class="seg" role="tablist">
      <button data-g="meal" class="on" role="tab">By meal type</button>
      <button data-g="cuisine" role="tab">By cuisine</button>
    </div>
    <div class="chips" id="quick"></div>
    <div class="chips" id="cats"></div>
  </div>
</div>
<main class="wrap">
  <div class="status"><span id="stat"></span><button id="reset" hidden>Clear filters</button></div>
  <div id="groups"></div>
</main>
<div id="detail" aria-modal="true" role="dialog"></div>
<div class="sticky-cta" id="stickycta"></div>
<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
const R = JSON.parse(document.getElementById('data').textContent);
const CATS = __CATS__;
const MEAL_ORDER = ["Breakfast","Lunch","Dinner/Mains","Soups & Stews","Sauces & Stocks","Sides","Appetizers","Desserts","Drinks"];
const MEAL_ICON = {"Breakfast":"☀️","Lunch":"🥗","Dinner/Mains":"🍽️","Soups & Stews":"🍲","Sauces & Stocks":"🥫","Sides":"🥦","Appetizers":"🧀","Desserts":"🥧","Drinks":"☕"};
const QUICK = [
  {k:"u45", label:"⏱ Under 45 min", f:r=>(r.total_time_min!=null && r.total_time_min<=45) || (r.total_time_min==null && (r.tags||[]).some(t=>t==="under-30-min"||t==="under-45-min"))},
  {k:"wn", label:"🌙 Weeknight", f:r=>r.occasion==="Weeknight"},
  {k:"kid", label:"🧒 Kid-friendly", f:r=>!!r.kid_friendly},
  {k:"fall", label:"🍂 Fall", f:r=>(r.tags||[]).includes("fall")},
];
const HOT = new Set(["Cajun & Creole","fall","under-30-min","under-45-min","one-pot","instant-pot","sauces","stock & base","gumbo","white chicken chili","Mexican","vegetarian"]);
const st = {q:"", group:"meal", cat:null, quick:new Set()};
const $ = s=>document.querySelector(s);
const esc = s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmt = m=>{ if(m==null) return null; if(m<60) return m+" min"; const h=Math.floor(m/60), mm=m%60; return h+" hr"+(mm?" "+mm+" min":""); };
const initials = n=>n.split(/\s+/).filter(w=>/^[A-Za-z]/.test(w)).slice(0,2).map(w=>w[0].toUpperCase()).join("");
R.forEach(r=>{ r._hay=[r.name,r.creator,r.source_name,r.cuisine,r.meal_type,r.main_protein,r.description,(r.tags||[]).join(" "),(r.categories||[]).join(" "),(r.key_ingredients||[]).join(" "),(r.ingredients||[]).join(" ")].join(" \u0001 ").toLowerCase(); });

function photo(r, cls){
  if(r.photo_local) return '<img src="'+esc(r.photo_local)+'" alt="'+esc(r.name)+'" loading="lazy" onerror="this.replaceWith(Object.assign(document.createElement(\'div\'),{className:\'noimg\',textContent:\''+esc(initials(r.name))+'\'}))">';
  return '<div class="noimg">'+esc(initials(r.name))+'<small>No photo</small></div>';
}
function pickTags(r){
  const t=(r.tags||[]); const hot=t.filter(x=>HOT.has(x)); const rest=t.filter(x=>!HOT.has(x));
  return hot.concat(rest).slice(0,2);
}
function card(r){
  const t=fmt(r.total_time_min);
  return '<button class="card" data-id="'+esc(r.id)+'" aria-label="'+esc(r.name)+'">'+
    '<div class="ph">'+photo(r)+(t?'<span class="time">⏱ '+esc(t)+'</span>':'')+'</div>'+
    '<div class="cb"><h3>'+esc(r.name)+'</h3><div class="by">by '+esc(r.creator)+'</div>'+
    '<div class="tags">'+pickTags(r).map(x=>'<span class="tag'+(HOT.has(x)?' hot':'')+'">'+esc(x)+'</span>').join("")+'</div></div></button>';
}
function filtered(){
  const words = st.q.toLowerCase().split(/\s+/).filter(Boolean);
  return R.filter(r=>{
    if(st.cat && !(r.categories||[]).includes(st.cat)) return false;
    for(const q of QUICK) if(st.quick.has(q.k) && !q.f(r)) return false;
    return words.every(w=>r._hay.includes(w));
  });
}
function render(){
  const list = filtered();
  $("#count").textContent = R.length+" recipes";
  const active = st.q || st.cat || st.quick.size;
  $("#stat").textContent = active ? (list.length+" of "+R.length+" match") : ("Showing all "+R.length);
  $("#reset").hidden = !active;
  $("#clear").style.display = st.q ? "block":"none";
  const groups = new Map();
  const key = st.group==="meal" ? (r=>r.meal_type||"Other") : (r=>r.cuisine||"Other");
  list.forEach(r=>{ const k=key(r); if(!groups.has(k)) groups.set(k,[]); groups.get(k).push(r); });
  let keys=[...groups.keys()];
  if(st.group==="meal") keys.sort((a,b)=>(MEAL_ORDER.indexOf(a)+99*(MEAL_ORDER.indexOf(a)<0))-(MEAL_ORDER.indexOf(b)+99*(MEAL_ORDER.indexOf(b)<0)));
  else keys.sort((a,b)=>groups.get(b).length-groups.get(a).length || a.localeCompare(b));
  if(!list.length){ $("#groups").innerHTML='<div class="empty">No recipes match.<br><br><button class="chip" id="reset2">Clear search & filters</button></div>'; $("#reset2").onclick=reset; return; }
  $("#groups").innerHTML = keys.map(k=>{
    const items = groups.get(k).slice().sort((a,b)=>a.name.localeCompare(b.name));
    const icon = st.group==="meal" ? (MEAL_ICON[k]||"") : "";
    return '<section class="group"><h2>'+(icon?'<span aria-hidden="true">'+icon+'</span>':'')+esc(k)+' <span class="n">'+items.length+'</span></h2><div class="grid">'+items.map(card).join("")+'</div></section>';
  }).join("");
}
function chips(){
  $("#quick").innerHTML = QUICK.map(q=>'<button class="chip quick'+(st.quick.has(q.k)?' on':'')+'" data-q="'+q.k+'">'+esc(q.label)+'</button>').join("");
  $("#cats").innerHTML = '<button class="chip'+(st.cat?'':' on')+'" data-c="">All</button>' + CATS.map(c=>'<button class="chip'+(st.cat===c?' on':'')+'" data-c="'+esc(c)+'">'+esc(c)+'</button>').join("");
}
function reset(){ st.q=""; st.cat=null; st.quick.clear(); $("#q").value=""; chips(); render(); }
$("#quick").addEventListener("click",e=>{ const b=e.target.closest("[data-q]"); if(!b) return; const k=b.dataset.q; st.quick.has(k)?st.quick.delete(k):st.quick.add(k); chips(); render(); });
$("#cats").addEventListener("click",e=>{ const b=e.target.closest("[data-c]"); if(!b) return; st.cat=b.dataset.c||null; chips(); render(); });
document.querySelectorAll(".seg button").forEach(b=>b.onclick=()=>{ st.group=b.dataset.g; document.querySelectorAll(".seg button").forEach(x=>x.classList.toggle("on",x===b)); render(); });
$("#q").addEventListener("input",e=>{ st.q=e.target.value.trim(); render(); });
$("#clear").onclick=()=>{ $("#q").value=""; st.q=""; render(); $("#q").focus(); };
$("#reset").onclick=reset;
let inApp=false;
$("#groups").addEventListener("click",e=>{ const c=e.target.closest(".card"); if(c){ inApp=true; location.hash="#/r/"+c.dataset.id; } });

function fact(k,v){ return v==null||v===""?"":'<div class="fact"><div class="k">'+esc(k)+'</div><div class="v">'+esc(v)+'</div></div>'; }
function detail(r){
  const t=(r.tags||[]), unavailable = !r.ingredients || !r.ingredients.length;
  const joeBits=[];
  if(r.rating!=null) joeBits.push('<span>Rating: <span class="stars">'+"★".repeat(r.rating)+"☆".repeat(Math.max(0,5-r.rating))+'</span></span>');
  if(r.times_made) joeBits.push('<span>Made '+r.times_made+'×</span>');
  if(r.last_made) joeBits.push('<span>Last made '+esc(r.last_made)+'</span>');
  if(r.make_again!=null) joeBits.push('<span>Make again: '+(r.make_again?"Yes":"No")+'</span>');
  const joe = (joeBits.length||r.changes_made) ? '<div class="d-sec"><h2>Joe\'s notes</h2><div class="note joe"><div class="row">'+joeBits.join("")+'</div>'+(r.changes_made?'<p style="margin:8px 0 0"><b>Changes:</b> '+esc(r.changes_made)+'</p>':'')+'</div></div>' : "";
  return '<button class="back" id="back" aria-label="Back"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button>'+
  '<div class="d-hero">'+photo(r)+'</div>'+
  '<div class="d-body">'+
    '<h1>'+esc(r.name)+'</h1>'+
    '<div class="credit">Recipe by <b>'+esc(r.creator)+'</b> · '+esc(r.source_name)+'</div>'+
    (r.description?'<p class="desc">'+esc(r.description)+'</p>':'')+
    '<a class="cta" href="'+esc(r.source_url)+'" target="_blank" rel="noopener">View original recipe ↗</a>'+
    '<div class="facts">'+fact("Total",fmt(r.total_time_min)||"—")+fact("Prep",fmt(r.prep_time_min)||"—")+fact("Cook",fmt(r.cook_time_min)||"—")+
      fact("Serves",r.servings==null?"—":r.servings)+fact("Difficulty",r.difficulty)+fact("Cuisine",r.cuisine)+
      fact("Protein",r.main_protein||"None / veg")+fact("Meal",r.meal_type)+fact("Method",r.cooking_method)+'</div>'+
    (unavailable?'<div class="d-sec unavail">Details unavailable from source — open the original recipe for ingredients and method.</div>':'')+
    (r.ingredients&&r.ingredients.length?'<div class="d-sec"><h2>Ingredients <small>tap to check off</small></h2><ul class="ing">'+r.ingredients.map(i=>'<li><span class="box"></span><span>'+esc(i)+'</span></li>').join("")+'</ul></div>':'')+
    (r.steps_summary&&r.steps_summary.length?'<div class="d-sec"><h2>Steps <small>summarized</small></h2><ol class="steps">'+r.steps_summary.map(s=>'<li>'+esc(s)+'</li>').join("")+'</ol></div>':'')+
    (r.notes?'<div class="d-sec"><h2>Notes</h2><div class="note">'+esc(r.notes)+'</div></div>':'')+
    joe+
    '<div class="d-sec"><h2>Tags</h2><div class="pill-row">'+(r.categories||[]).map(c=>'<span class="chip on" style="padding:4px 10px;font-size:12px">'+esc(c)+'</span>').join("")+t.map(x=>'<span class="tag'+(HOT.has(x)?' hot':'')+'" style="font-size:12px;padding:4px 8px">'+esc(x)+'</span>').join("")+'</div></div>'+
    '<div class="src">Credit: '+esc(r.creator)+' — <a href="'+esc(r.source_url)+'" target="_blank" rel="noopener">'+esc(r.source_url)+'</a><br>Added '+esc(r.date_added)+'</div>'+
  '</div>';
}
let lastScroll=0;
function route(){
  const m = location.hash.match(/^#\/r\/(.+)$/);
  const d=$("#detail"), sc=$("#stickycta");
  if(m){
    const r=R.find(x=>x.id===decodeURIComponent(m[1]));
    if(!r){ location.hash=""; return; }
    if(!d.classList.contains("open")) lastScroll=window.scrollY;
    d.innerHTML=detail(r); d.scrollTop=0; d.classList.add("open"); document.body.classList.add("lock");
    sc.innerHTML='<a class="cta" href="'+esc(r.source_url)+'" target="_blank" rel="noopener">View original recipe ↗</a>';
    $("#back").onclick=()=>{ if(inApp){ inApp=false; history.back(); } else location.hash=""; };
    d.querySelectorAll("ul.ing li").forEach(li=>li.onclick=()=>li.classList.toggle("done"));
    sc.classList.remove("show");
    if(window.IntersectionObserver){ if(window._io) window._io.disconnect(); window._io=new IntersectionObserver(es=>{ es.forEach(en=>sc.classList.toggle("show", !en.isIntersecting && en.boundingClientRect.top<0)); },{root:d}); window._io.observe(d.querySelector(".d-body .cta")); }
    else sc.classList.add("show");
    document.title=r.name+" · Joe's Recipe Box";
  } else {
    d.classList.remove("open"); d.innerHTML=""; sc.innerHTML=""; document.body.classList.remove("lock");
    window.scrollTo(0,lastScroll); document.title="Joe's Recipe Box";
  }
}
document.addEventListener("keydown",e=>{ if(e.key==="Escape" && $("#detail").classList.contains("open")) location.hash=""; });
window.addEventListener("hashchange",route);
chips(); render(); route();
})();
</script>
</body>
</html>
"""
out = TEMPLATE.replace("__DATA__", data).replace("__CATS__", json.dumps(used))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print(f"index.html written: {len(recipes)} recipes, {len(out)//1024} KB")

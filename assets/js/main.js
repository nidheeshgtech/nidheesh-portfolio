/* Nidheesh Narayanan — portfolio interactions (vanilla JS; Lenis for smooth scrolling) */
(() => {
  const root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');
  const hasLoader = root.classList.contains('has-loader');

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- analytics: GA4 (gtag) or Google Tag Manager (dataLayer); harmless with neither ----------
     events: contact_click {contact_method, link_location} · email_copy · case_study_click {project, link_location}
             outbound_click {link_url} · section_view {section} · faq_open {question} */
  window.dataLayer = window.dataLayer || [];
  // GA4 direct (gtag on the page) gets real GA events; with GTM the dataLayer push feeds its triggers
  const track = (event, data = {}) => (typeof window.gtag === 'function' ? window.gtag('event', event, data) : window.dataLayer.push({ event, ...data }));
  const whereIs = (el) => {
    const zone = el.closest('.site-header, .menu, .hero, .projects, .more, .case-head, .case-next, .footer, .services, .faq__list');
    return zone ? zone.className.split(' ')[0].replace(/^site-/, '') : 'page';
  };
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href');
    const loc = whereIs(a);
    if (href.startsWith('mailto:')) return track('contact_click', { contact_method: 'email', link_location: loc });
    if (href.includes('linkedin.com/')) return track('contact_click', { contact_method: 'linkedin', link_location: loc });
    if (/(^|\/)work\/[a-z0-9-]+(\.html)?$/.test(href) || (a.closest('.case-next'))) {
      const name = a.querySelector('.project__name, .more__name, .case-next__name');
      return track('case_study_click', { project: (name ? name.firstChild.textContent : a.textContent).trim(), link_location: loc });
    }
    if (/^https?:\/\//.test(href) && !href.includes(location.hostname)) return track('outbound_click', { link_url: href, link_location: loc });
  });
  document.addEventListener('toggle', (e) => {
    if (e.target.matches && e.target.matches('details.qa') && e.target.open) track('faq_open', { question: e.target.querySelector('summary').textContent.trim() });
  }, true);
  if ('IntersectionObserver' in window) {
    const seen = new Set();
    const so = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (!en.isIntersecting || seen.has(en.target.id)) return;
      seen.add(en.target.id);
      track('section_view', { section: en.target.id });
      so.unobserve(en.target);
    }), { threshold: 0.35 });
    ['work', 'services', 'about', 'contact'].forEach((id) => { const s = document.getElementById(id); if (s) so.observe(s); });
  }

  /* ---------- Dubai clock + year ---------- */
  const clocks = $$('[data-clock]');
  const fmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Dubai' });
  const tick = () => { const t = fmt.format(new Date()); clocks.forEach((c) => (c.textContent = t)); };
  tick();
  setInterval(tick, 15000);
  $$('[data-year]').forEach((el) => (el.textContent = new Date().getFullYear()));

  /* ---------- smooth scrolling (Lenis) ---------- */
  let lenis = null;
  if (window.Lenis && !reduced) {
    lenis = new window.Lenis({ lerp: 0.1, smoothWheel: true, wheelMultiplier: 0.95 });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  const scrollToEl = (el) => {
    if (lenis) lenis.scrollTo(el || 0, { offset: el ? -20 : 0 });
    else if (el) el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
    else window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
  };
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href');
    if (id === '#main') return; // skip link: let the browser move focus
    const el = id === '#top' ? null : document.querySelector(id);
    if (id !== '#top' && !el) return;
    e.preventDefault();
    scrollToEl(el);
    if (id !== '#top') history.replaceState(null, '', id);
  });

  /* ---------- header colour over dark areas ---------- */
  const header = $('#header');
  const menu = $('#menu');
  let headerDark = false;
  const darkSections = $$('[data-theme="dark"]');
  const setHeaderDark = (on) => {
    if (on === headerDark) return;
    headerDark = on;
    if (menu.hidden) header.classList.toggle('on-dark', on);
  };

  /* ---------- mobile menu ---------- */
  const toggle = $('.menu-toggle');
  const setMenu = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
    document.body.style.overflow = open ? 'hidden' : '';
    if (lenis) { if (open) lenis.stop(); else lenis.start(); }
    menu.hidden = !open;
    menu.inert = !open;
    header.classList.toggle('on-dark', open ? false : headerDark);
    if (open) { const first = $('nav a', menu); if (first) first.focus(); }
  };
  toggle.addEventListener('click', () => setMenu(menu.hidden));
  $$('a', menu).forEach((a) => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !menu.hidden) { setMenu(false); toggle.focus(); }
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 1000 && !menu.hidden) setMenu(false); });

  /* ---------- big name: fit to the width of its container ---------- */
  const fitWordmarks = () => {
    $$('[data-fit]').forEach((el) => {
      const inner = $('.wordmark__inner', el);
      const cs = getComputedStyle(el.parentElement);
      const avail = el.parentElement.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      el.style.fontSize = '100px';
      const w = inner.getBoundingClientRect().width;
      if (w > 0) el.style.fontSize = `${Math.floor((avail / w) * 100 * 0.99)}px`;
    });
  };

  /* ---------- phone headline: each line scaled to fill the width ---------- */
  const fitLines = () => {
    $$('[data-fit-lines]').forEach((h) => {
      const lines = $$('.hl', h);
      if (window.innerWidth > 760) { lines.forEach((l) => { l.style.fontSize = ''; }); return; }
      const avail = h.clientWidth;
      lines.forEach((l) => {
        l.style.fontSize = '100px';
        const w = l.getBoundingClientRect().width;
        if (w > 0) l.style.fontSize = `${Math.min(140, Math.floor((avail / w) * 100 * 0.985))}px`;
      });
    });
  };

  /* ---------- split text into words + characters (for the scroll reveal) ---------- */
  $$('[data-split], [data-split-scroll]').forEach((el) => {
    const blocks = el.children.length ? [...el.children] : [el];
    let i = 0;
    blocks.forEach((block) => {
      const label = block.textContent.trim();
      block.textContent = '';
      label.split(/\s+/).forEach((w, k) => {
        if (k) block.appendChild(document.createTextNode(' '));
        const ws = document.createElement('span');
        ws.className = 'w';
        ws.setAttribute('aria-hidden', 'true');
        [...w].forEach((ch) => {
          const c = document.createElement('span');
          c.className = 'c';
          c.textContent = ch;
          c.style.setProperty('--i', i++);
          ws.appendChild(c);
        });
        block.appendChild(ws);
      });
      const sr = document.createElement('span');
      sr.className = 'sr-only';
      sr.textContent = label;
      block.appendChild(sr);
    });
    el.style.setProperty('--n', i);
  });

  /* ---------- statements: three lines, one after another, while the background turns light ---------- */
  const st = $('[data-statements]');
  const lines = st ? $$('.statement', st) : [];
  let stDark = false;
  const updateStatements = () => {
    if (!st || reduced) return;
    const r = st.getBoundingClientRect();
    const travel = st.offsetHeight - window.innerHeight;
    const p = clamp(-r.top / travel);
    const seg = 1 / lines.length;
    lines.forEach((line, i) => {
      const t = (p - i * seg) / seg;                 // where we are inside this line's share of the scroll
      const last = i === lines.length - 1;
      // lines never overlap: the old one is gone before the next one comes in
      const inO = i === 0 ? clamp((-r.top / window.innerHeight + 0.6) / 0.4) : clamp((t - 0.04) / 0.12);
      const outO = last ? 1 : 1 - clamp((t - 0.78) / 0.16);
      line.style.setProperty('--p', clamp((t - 0.06) / 0.56).toFixed(3));
      line.style.setProperty('--o', (inO * outO).toFixed(3));
      line.style.setProperty('--y', `${((1 - inO) * 28 - (1 - outO) * 28).toFixed(1)}px`);
    });
    const darkO = 1 - clamp((p - 0.6) / 0.12);
    st.style.setProperty('--dark-o', darkO.toFixed(3));
    stDark = r.top <= 30 && r.bottom > 30 && darkO > 0.5;
  };

  /* ---------- paragraph reveal: characters light up as it moves up the screen ---------- */
  const scrollSplits = $$('[data-split-scroll]');
  const updateSplits = () => {
    const vh = window.innerHeight;
    scrollSplits.forEach((el) => {
      const r = el.getBoundingClientRect();
      const p = reduced ? 1 : clamp((vh * 0.92 - r.top) / (vh * 0.5));
      el.style.setProperty('--p', p.toFixed(3));
    });
  };

  const heroEl = $('.hero');
  const onScroll = () => {
    updateStatements();
    updateSplits();
    header.classList.toggle('is-scrolled', window.scrollY > 10);
    if (heroEl && !reduced && window.scrollY < window.innerHeight * 1.2) {
      heroEl.style.setProperty('--hero-shift', `${(window.scrollY * 0.12).toFixed(1)}px`);
      root.classList.toggle('is-shifting', window.scrollY > 0);
    }
    const y = 30;
    const overDark = stDark || darkSections.some((s) => { const r = s.getBoundingClientRect(); return r.top <= y && r.bottom > y; });
    setHeaderDark(overDark);
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- services: the item in the middle of the screen is active ---------- */
  const services = $$('[data-service]');
  const media = $$('.services__media img');
  if (services.length && 'IntersectionObserver' in window) {
    const setActive = (i) => {
      services.forEach((s, k) => s.classList.toggle('is-active', k === i));
      media.forEach((m, k) => m.classList.toggle('is-active', k === i));
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) setActive(Number(e.target.dataset.service)); });
    }, { rootMargin: '-48% 0px -48% 0px' });
    services.forEach((s) => io.observe(s));
  }

  /* ---------- active nav link ---------- */
  const links = $$('.site-nav a').filter((a) => a.getAttribute('href').startsWith('#'));
  if (links.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        links.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === `#${e.target.id}`));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.map((a) => $(a.getAttribute('href'))).filter(Boolean).forEach((s) => io.observe(s));
  }

  /* ---------- copy email address ---------- */
  $$('[data-copy]').forEach((btn) => {
    const status = $('[data-copy-status]');
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.copy);
        track('email_copy', { link_location: whereIs(btn) });
        btn.textContent = 'Copied';
        btn.classList.add('is-done');
        if (status) status.textContent = 'Email address copied';
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.toggle('is-done', false); if (status) status.textContent = ''; }, 2000);
      } catch (e) {
        window.location.href = `mailto:${btn.dataset.copy}`;
      }
    });
  });

  /* ---------- English / Arabic comparison slider (case-study pages) ---------- */
  $$('[data-compare]').forEach((box) => {
    const range = $('input', box);
    const set = () => box.style.setProperty('--pos', `${range.value}%`);
    range.addEventListener('input', set);
    set();
  });

  /* ---------- hero light flare: a small WebGL shader behind the portrait ----------
     Soft rays from a light behind the head, a lens streak, a sweeping band, haze and drifting bokeh.
     Rendered at half resolution, paused when the banner is off screen or the tab is hidden. */
  const hero = $('.hero');
  if (hero) {
    const cv = document.createElement('canvas');
    cv.className = 'hero__flare';
    cv.setAttribute('aria-hidden', 'true');
    const gl = cv.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false, powerPreference: 'low-power' });
    if (gl) {
      hero.prepend(cv);
      hero.classList.add('has-flare');
      const vs = 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';
      const fs = `precision mediump float;
uniform vec2 r;uniform float t;uniform vec2 m;uniform float small;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+1.),f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<4;i++){v+=a*n(p);p*=2.03;a*=.5;}return v;}
void main(){
  vec2 uv=gl_FragCoord.xy/r;float asp=r.x/r.y;vec2 p=vec2(uv.x*asp,uv.y);
  vec2 src=vec2(mix(.70,.78,small)*asp,mix(.80,.86,small))+.025*vec2(sin(t*.13),cos(t*.11))+m*vec2(.05,.03);
  vec2 d=p-src;float dist=length(d);vec2 dir=d/max(dist,1e-4);
  float rays=pow(fbm(dir*3.1+vec2(t*.035,-t*.028)),3.4)*2.8;
  rays+=.6*pow(n(dir*13.+vec2(t*.05,t*.04)),6.);
  rays*=exp(-dist*1.35)*smoothstep(0.,.12,dist);
  float core=exp(-dist*dist*14.);
  float sweep=exp(-pow((p.x*.85+p.y*.55)-(1.05+.38*sin(t*.07)),2.)*22.)*.32;
  float streak=exp(-d.y*d.y*900.)*exp(-abs(d.x)*3.)*.22;
  float haze=fbm(p*1.5+vec2(t*.018,-t*.012))*exp(-dist*1.1)*.22;
  float fade=smoothstep(.04,.42,uv.y);
  float light=(rays*.6+core*.5+sweep+streak+haze)*fade;
  vec3 base=vec3(.925,.925,.922);
  vec3 tint=mix(vec3(1.,.965,.92),vec3(.92,.96,1.),smoothstep(0.,.9,dist));
  vec3 col=base-vec3(.07)*smoothstep(.15,1.1,dist)*fade+light*.2*tint;
  for(int i=0;i<12;i++){float fi=float(i);
    vec2 bp=vec2(h(vec2(fi,1.7))*asp,fract(h(vec2(fi,2.3))+t*.012*(.4+h(vec2(fi,3.1)))));
    float s=.008+.028*h(vec2(fi,4.9));
    float b=smoothstep(s,s*.55,length(p-bp));
    col+=b*.045*tint*fade;}
  col+=(h(gl_FragCoord.xy+fract(t))-.5)*.012;
  gl_FragColor=vec4(min(col,vec3(1.)),1.);
}`;
      const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
      const prog = gl.createProgram();
      gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs));
      gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
        cv.remove(); hero.classList.remove('has-flare');
      } else {
        gl.useProgram(prog);
        const buf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
        const loc = gl.getAttribLocation(prog, 'a');
        gl.enableVertexAttribArray(loc);
        gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
        const uR = gl.getUniformLocation(prog, 'r'), uT = gl.getUniformLocation(prog, 't');
        const uM = gl.getUniformLocation(prog, 'm'), uS = gl.getUniformLocation(prog, 'small');
        const SCALE = 0.5;
        const size = () => {
          const w = Math.max(1, Math.round(hero.clientWidth * SCALE)), hgt = Math.max(1, Math.round(hero.clientHeight * SCALE));
          if (cv.width !== w || cv.height !== hgt) { cv.width = w; cv.height = hgt; gl.viewport(0, 0, w, hgt); }
          gl.uniform2f(uR, w, hgt);
          gl.uniform1f(uS, window.innerWidth < 760 ? 1 : 0);
        };
        size();
        const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
        hero.addEventListener('pointermove', (e) => {
          if (e.pointerType !== 'mouse') return;
          mouse.tx = e.clientX / window.innerWidth - 0.5;
          mouse.ty = 0.5 - e.clientY / window.innerHeight;
        });
        let visible = true, frameId = null;
        const t0 = performance.now();
        const draw = (now) => {
          frameId = null;
          mouse.x += (mouse.tx - mouse.x) * 0.04;
          mouse.y += (mouse.ty - mouse.y) * 0.04;
          gl.uniform1f(uT, reduced ? 12 : (now - t0) / 1000);
          gl.uniform2f(uM, mouse.x, mouse.y);
          gl.drawArrays(gl.TRIANGLES, 0, 3);
          if (!reduced && visible && !document.hidden) frameId = requestAnimationFrame(draw);
        };
        const play = () => { if (!frameId) frameId = requestAnimationFrame(draw); };
        if ('IntersectionObserver' in window) {
          new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) play(); }).observe(hero);
        }
        document.addEventListener('visibilitychange', () => { if (!document.hidden) play(); });
        let rs;
        window.addEventListener('resize', () => { clearTimeout(rs); rs = setTimeout(() => { size(); play(); }, 150); });
        play();
      }
    }
  }

  /* ---------- start: show the banner straight away (good LCP), refit the name when the web font arrives ---------- */
  fitWordmarks();
  fitLines();
  onScroll();
  /* ---------- loader: counts real progress (fonts, hero photo, page load), then wipes up ---------- */
  const reveal = () => requestAnimationFrame(() => root.classList.add('is-ready'));
  const loaderEl = $('.loader');
  if (hasLoader && loaderEl) {
    if (lenis) lenis.stop();
    const pctEl = $('[data-loader-pct]', loaderEl);
    const tasks = [];
    if (document.fonts && document.fonts.ready) tasks.push(document.fonts.ready);
    const heroImg = $('.hero__photo');
    if (heroImg && !heroImg.complete) tasks.push(new Promise((r) => { heroImg.addEventListener('load', r, { once: true }); heroImg.addEventListener('error', r, { once: true }); }));
    if (document.readyState !== 'complete') tasks.push(new Promise((r) => window.addEventListener('load', r, { once: true })));
    let done = 0, shown = 0, finished = false;
    const total = Math.max(1, tasks.length);
    tasks.forEach((t) => Promise.resolve(t).catch(() => {}).then(() => { done++; }));
    const t0 = performance.now();
    const MIN = 1300, MAX = 4500;
    const finish = () => {
      if (finished) return;
      finished = true;
      try { sessionStorage.setItem('nn-seen', '1'); } catch (e) {}
      loaderEl.classList.add('is-done');
      setTimeout(() => {
        root.classList.remove('has-loader');
        if (lenis) lenis.start();
        reveal();
        loaderEl.remove();
      }, 1050);
    };
    const step = (now) => {
      const elapsed = now - t0;
      const real = done / total;                                 // share of things actually loaded
      const timeCap = Math.min(1, elapsed / MIN);                // never faster than MIN
      let target = Math.min(real, timeCap) * 100;
      if (real < 1) target = Math.min(target, 92 + 7 * (elapsed / MAX)); // creep while waiting
      if (elapsed > MAX) target = 100;
      shown += (target - shown) * 0.12 + (target > shown ? 0.15 : 0);
      shown = Math.min(shown, target);
      const v = Math.round(shown);
      pctEl.textContent = `${v}%`;
      loaderEl.style.setProperty('--p', v);
      if (v >= 100) { setTimeout(finish, 180); return; }
      requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  } else {
    if (loaderEl) loaderEl.remove();
    reveal();
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { fitWordmarks(); fitLines(); }).catch(() => {});
  let rt;
  window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { fitWordmarks(); fitLines(); onScroll(); }, 120); });
})();

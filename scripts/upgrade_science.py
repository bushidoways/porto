from pathlib import Path
import json

INDEX = Path('index.html')
DATA = Path('science-facts.json')
html = INDEX.read_text(encoding='utf-8')

CSS = r'''
/* ── SCIENCE FLASHCARD WIDGET — LEFT BOTTOM ─────────── */
.sf-widget{position:fixed;left:var(--space-6);bottom:var(--space-6);z-index:201;width:min(340px,calc(100vw - 2rem));background:var(--bg-soft);color:var(--text);border:1px solid var(--border);border-radius:var(--radius-xl);box-shadow:var(--shadow-lg);overflow:hidden;animation:sf-pop-in 180ms cubic-bezier(.16,1,.3,1)}
.sf-widget[hidden]{display:none}@keyframes sf-pop-in{from{opacity:0;transform:translateY(12px) scale(.97)}to{opacity:1;transform:none}}
.sf-header{display:flex;align-items:center;justify-content:space-between;gap:var(--space-3);padding:var(--space-3) var(--space-4);background:var(--text);color:var(--text-inverse)}
.sf-header-left,.sf-header-actions{display:flex;align-items:center;gap:var(--space-2)}.sf-header-icon{width:24px;height:24px;display:grid;place-items:center;flex:0 0 auto;border-radius:50%;background:rgba(255,255,255,.1);color:var(--accent)}
.sf-header-title{font-family:var(--font-mono);font-size:.75rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:rgba(250,247,242,.75)}
.sf-icon-btn{width:44px;height:44px;display:grid;place-items:center;border-radius:var(--radius-sm);color:rgba(250,247,242,.55);font-size:1rem;line-height:1}.sf-icon-btn:hover{background:rgba(255,255,255,.1);color:var(--text-inverse)}
.sf-body{padding:var(--space-5)}.sf-category{display:inline-flex;align-items:center;margin-bottom:var(--space-3);padding:3px 9px;border:1px solid var(--accent-border);border-radius:var(--radius-full);background:var(--accent-soft);color:var(--accent-hover);font-family:var(--font-mono);font-size:.75rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase}
.sf-title{margin-bottom:var(--space-3);font-family:var(--font-display);font-size:clamp(1.45rem,4vw,1.8rem);font-weight:400;line-height:1.1;letter-spacing:-.025em;color:var(--text)}.sf-fact{margin-bottom:var(--space-4);color:var(--text-muted);font-size:.82rem;line-height:1.75}
.sf-source{display:inline-flex;align-items:center;gap:5px;margin-bottom:var(--space-4);color:var(--text-faint);font-family:var(--font-mono);font-size:.75rem;line-height:1.5}.sf-source:hover{color:var(--accent-hover)}
.sf-footer{display:flex;gap:var(--space-2);padding-top:var(--space-4);border-top:1px solid var(--divider)}.sf-next-btn,.sf-source-btn{min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:var(--space-2);border-radius:var(--radius-md);font-size:.75rem;font-weight:600}
.sf-next-btn{flex:1;background:var(--text);color:var(--text-inverse)}.sf-next-btn:hover{background:var(--accent);transform:translateY(-1px)}.sf-next-btn:disabled{opacity:.55;cursor:wait;transform:none}.sf-source-btn{width:44px;border:1px solid var(--border-strong);color:var(--text-muted)}.sf-source-btn:hover{border-color:var(--accent-border);background:var(--accent-soft);color:var(--accent-hover)}
.sf-pill{position:fixed;left:var(--space-6);bottom:var(--space-6);z-index:200;width:50px;height:50px;display:grid;place-items:center;border-radius:50%;background:var(--text);color:var(--text-inverse);box-shadow:var(--shadow-md)}.sf-pill[hidden]{display:none}.sf-pill:hover{background:var(--accent);transform:translateY(-3px);box-shadow:var(--shadow-lg)}.sf-pill svg{width:22px;height:22px}
@media(max-width:480px){.sf-widget{left:var(--space-4);bottom:var(--space-4);width:calc(100vw - var(--space-8))}.sf-pill{left:var(--space-4);bottom:var(--space-4)}}@media(prefers-reduced-motion:reduce){.sf-widget{animation:none}}
'''

WIDGET = r'''
<!-- SCIENCE FLASHCARD WIDGET -->
<aside id="science-widget" class="sf-widget" hidden aria-labelledby="science-title" aria-live="polite">
  <div class="sf-header"><div class="sf-header-left"><span class="sf-header-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="1.8" fill="currentColor"></circle><ellipse cx="12" cy="12" rx="9" ry="3.8"></ellipse><ellipse cx="12" cy="12" rx="9" ry="3.8" transform="rotate(60 12 12)"></ellipse><ellipse cx="12" cy="12" rx="9" ry="3.8" transform="rotate(120 12 12)"></ellipse></svg></span><span class="sf-header-title">Fakta Sains</span></div><div class="sf-header-actions"><button id="science-minimize" class="sf-icon-btn" type="button" aria-label="Sembunyikan fakta sains" title="Sembunyikan">−</button><button id="science-close" class="sf-icon-btn" type="button" aria-label="Tutup fakta sains" title="Tutup">×</button></div></div>
  <div class="sf-body"><div id="science-category" class="sf-category">Memuat fakta</div><h2 id="science-title" class="sf-title">Fakta sains sedang disiapkan.</h2><p id="science-fact" class="sf-fact">Tunggu sebentar.</p><a id="science-source" class="sf-source" href="#" target="_blank" rel="noopener noreferrer" aria-label="Buka sumber fakta sains"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 3h7v7"></path><path d="M10 14 21 3"></path><path d="M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5"></path></svg><span id="science-source-label">Sumber tervalidasi</span></a><div class="sf-footer"><button id="science-next" class="sf-next-btn" type="button">Fakta lain <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></button><a id="science-source-btn" class="sf-source-btn" href="#" target="_blank" rel="noopener noreferrer" aria-label="Lihat sumber" title="Lihat sumber">↗</a></div></div>
</aside>
<button id="science-pill" class="sf-pill" type="button" aria-label="Buka fakta sains" title="Fakta sains yang mungkin belum kamu tahu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="1.8" fill="currentColor"></circle><ellipse cx="12" cy="12" rx="9" ry="3.8"></ellipse><ellipse cx="12" cy="12" rx="9" ry="3.8" transform="rotate(60 12 12)"></ellipse><ellipse cx="12" cy="12" rx="9" ry="3.8" transform="rotate(120 12 12)"></ellipse></svg></button>
'''

JS = r'''
// ── SCIENCE FLASHCARD WIDGET ───────────────────────
(() => {
  const fallback=[{"category":"Astronomi","title":"Venus berotasi sangat lambat.","fact":"Satu rotasi Venus membutuhkan sekitar 243 hari Bumi, lebih lama daripada satu orbitnya.","sourceLabel":"NASA Science","sourceUrl":"https://science.nasa.gov/venus/facts/"},{"category":"Fisika","title":"Es mengapung karena kurang rapat.","fact":"Struktur kristal es membuat air padat kurang rapat daripada air cair.","sourceLabel":"USGS","sourceUrl":"https://www.usgs.gov/special-topics/water-science-school"}];
  const el=id=>document.getElementById(id),widget=el('science-widget'),pill=el('science-pill'),category=el('science-category'),title=el('science-title'),fact=el('science-fact'),source=el('science-source'),sourceLabel=el('science-source-label'),sourceBtn=el('science-source-btn'),nextBtn=el('science-next'),minimize=el('science-minimize'),close=el('science-close'); if(!widget||!pill)return;
  let facts=[],current=-1,deck=[],cursor=0; const day=()=>Math.floor((Date.now()-new Date(new Date().getFullYear(),0,0))/86400000);
  function shuffle(){deck=Array.from({length:facts.length},(_,i)=>i);for(let i=deck.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[deck[i],deck[j]]=[deck[j],deck[i]]}if(deck[0]===current&&deck.length>1)[deck[0],deck[1]]=[deck[1],deck[0]];cursor=0}
  function render(i){const x=facts[i];if(!x)return;category.textContent=x.category;title.textContent=x.title;fact.textContent=x.fact;source.href=x.sourceUrl;sourceLabel.textContent=`Sumber: ${x.sourceLabel}`;sourceBtn.href=x.sourceUrl;current=i}
  function next(){if(cursor>=deck.length)shuffle();render(deck[cursor++])} function open(){widget.hidden=false;pill.hidden=true;minimize.focus()} function hide(){widget.hidden=true;pill.hidden=false;pill.focus()}
  async function init(){nextBtn.disabled=true;try{const r=await fetch('./science-facts.json',{cache:'no-cache'});if(!r.ok)throw Error(r.status);facts=await r.json();if(!Array.isArray(facts)||!facts.length)throw Error('empty')}catch(e){console.warn('Memakai fakta cadangan',e);facts=fallback}render(day()%facts.length);shuffle();nextBtn.disabled=false}
  pill.addEventListener('click',open);minimize.addEventListener('click',hide);close.addEventListener('click',hide);nextBtn.addEventListener('click',next);document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!widget.hidden)hide()});init();
})();
'''

if 'SCIENCE FLASHCARD WIDGET — LEFT BOTTOM' not in html:
    html = html.replace('/* ── REVEAL ANIMATIONS', CSS + '\n/* ── REVEAL ANIMATIONS', 1)
if '<!-- SCIENCE FLASHCARD WIDGET -->' not in html:
    html = html.replace('<!-- DAILY VERSE WIDGET -->', WIDGET + '\n<!-- DAILY VERSE WIDGET -->', 1)
if '// ── SCIENCE FLASHCARD WIDGET' not in html:
    html = html.replace('// ── DAILY VERSE', JS + '\n// ── DAILY VERSE', 1)
INDEX.write_text(html, encoding='utf-8')

facts=[]
def add(category,title,fact,label,url):
    facts.append({'id':len(facts)+1,'category':category,'title':title,'fact':fact,'sourceLabel':label,'sourceUrl':url})

nist='NIST — Periodic Table'; nist_url='https://www.nist.gov/blogs/taking-measure/periodic-table-its-more-just-chemistry-and-physics'
elements='H:Hydrogen,He:Helium,Li:Lithium,Be:Beryllium,B:Boron,C:Carbon,N:Nitrogen,O:Oxygen,F:Fluorine,Ne:Neon,Na:Sodium,Mg:Magnesium,Al:Aluminium,Si:Silicon,P:Phosphorus,S:Sulfur,Cl:Chlorine,Ar:Argon,K:Potassium,Ca:Calcium,Sc:Scandium,Ti:Titanium,V:Vanadium,Cr:Chromium,Mn:Manganese,Fe:Iron,Co:Cobalt,Ni:Nickel,Cu:Copper,Zn:Zinc,Ga:Gallium,Ge:Germanium,As:Arsenic,Se:Selenium,Br:Bromine,Kr:Krypton,Rb:Rubidium,Sr:Strontium,Y:Yttrium,Zr:Zirconium,Nb:Niobium,Mo:Molybdenum,Tc:Technetium,Ru:Ruthenium,Rh:Rhodium,Pd:Palladium,Ag:Silver,Cd:Cadmium,In:Indium,Sn:Tin,Sb:Antimony,Te:Tellurium,I:Iodine,Xe:Xenon,Cs:Caesium,Ba:Barium,La:Lanthanum,Ce:Cerium,Pr:Praseodymium,Nd:Neodymium,Pm:Promethium,Sm:Samarium,Eu:Europium,Gd:Gadolinium,Tb:Terbium,Dy:Dysprosium,Ho:Holmium,Er:Erbium,Tm:Thulium,Yb:Ytterbium,Lu:Lutetium,Hf:Hafnium,Ta:Tantalum,W:Tungsten,Re:Rhenium,Os:Osmium,Ir:Iridium,Pt:Platinum,Au:Gold,Hg:Mercury,Tl:Thallium,Pb:Lead,Bi:Bismuth,Po:Polonium,At:Astatine,Rn:Radon,Fr:Francium,Ra:Radium,Ac:Actinium,Th:Thorium,Pa:Protactinium,U:Uranium,Np:Neptunium,Pu:Plutonium,Am:Americium,Cm:Curium,Bk:Berkelium,Cf:Californium,Es:Einsteinium,Fm:Fermium,Md:Mendelevium,No:Nobelium,Lr:Lawrencium,Rf:Rutherfordium,Db:Dubnium,Sg:Seaborgium,Bh:Bohrium,Hs:Hassium,Mt:Meitnerium,Ds:Darmstadtium,Rg:Roentgenium,Cn:Copernicium,Nh:Nihonium,Fl:Flerovium,Mc:Moscovium,Lv:Livermorium,Ts:Tennessine,Og:Oganesson'
for number,item in enumerate(elements.split(','),1):
    symbol,name=item.split(':')
    add('Kimia',f'Unsur ke-{number}: {name}.',f'{name} memiliki simbol kimia {symbol} dan nomor atom {number}; nomor atom menyatakan jumlah proton di intinya.',nist,nist_url)

nasa='NASA Science'; nasa_url='https://science.nasa.gov/solar-system/planets/'
planets=[
('Merkurius','pertama','planet kebumian','sekitar 59 hari Bumi','planet terkecil dan paling dekat dengan Matahari'),
('Venus','kedua','planet kebumian','sekitar 243 hari Bumi','planet terpanas karena efek rumah kaca yang kuat'),
('Bumi','ketiga','planet kebumian','sekitar 23,9 jam','satu-satunya dunia yang diketahui memiliki kehidupan'),
('Mars','keempat','planet kebumian','sekitar 24,6 jam','memiliki Olympus Mons, gunung berapi terbesar yang diketahui di Tata Surya'),
('Jupiter','kelima','raksasa gas','sekitar 9,9 jam','planet terbesar dan memiliki Bintik Merah Besar'),
('Saturnus','keenam','raksasa gas','sekitar 10,7 jam','memiliki sistem cincin paling mencolok'),
('Uranus','ketujuh','raksasa es','sekitar 17 jam','berotasi hampir menyamping dengan kemiringan sumbu sekitar 98 derajat'),
('Neptunus','kedelapan','raksasa es','sekitar 16 jam','memiliki angin atmosfer yang luar biasa cepat')]
for name,order,kind,rotation,feature in planets:
    add('Astronomi',f'{name} adalah planet {order} dari Matahari.',f'Urutan orbit {name} menempatkannya sebagai planet {order} jika dihitung keluar dari Matahari.',nasa,nasa_url)
    add('Astronomi',f'{name} termasuk {kind}.',f'Berdasarkan komposisi dan strukturnya, {name} diklasifikasikan sebagai {kind}.',nasa,nasa_url)
    add('Astronomi',f'Lama rotasi {name}: {rotation}.',f'{name} menyelesaikan satu putaran pada sumbunya dalam {rotation}.',nasa,nasa_url)
    add('Astronomi',f'Ciri khas {name}.',f'{name} {feature}.',nasa,nasa_url)

dwarfs=[('Ceres','berada di sabuk asteroid antara Mars dan Jupiter'),('Pluto','direklasifikasi sebagai planet katai pada 2006'),('Haumea','berbentuk lonjong dan berotasi sangat cepat'),('Makemake','merupakan salah satu objek terang di Sabuk Kuiper'),('Eris','berada jauh di kawasan luar Tata Surya')]
for name,feature in dwarfs:
    add('Astronomi',f'{name} adalah planet katai.',f'{name} termasuk salah satu dari lima planet katai yang diakui resmi di Tata Surya.',nasa,nasa_url)
    add('Astronomi',f'Lokasi dan ciri {name}.',f'{name} {feature}.',nasa,nasa_url)

nih='NIH MedlinePlus'; nih_url='https://medlineplus.gov/anatomy.html'
organs=[
('Jantung','sistem kardiovaskular','memompa darah ke paru-paru dan seluruh tubuh'),('Paru-paru','sistem pernapasan','menukar oksigen dan karbon dioksida'),('Otak','sistem saraf','memproses informasi dan mengoordinasikan banyak fungsi tubuh'),('Sumsum tulang belakang','sistem saraf','membawa sinyal antara otak dan tubuh serta menangani beberapa refleks'),('Hati','sistem pencernaan','memproses nutrien, menghasilkan empedu, dan membantu detoksifikasi'),('Ginjal','sistem urinaria','menyaring darah dan mengatur air, elektrolit, serta limbah'),('Lambung','sistem pencernaan','mencampur makanan dengan asam dan enzim'),('Usus halus','sistem pencernaan','menjadi lokasi utama pencernaan lanjutan dan penyerapan nutrien'),('Usus besar','sistem pencernaan','menyerap air dan membentuk feses'),('Pankreas','sistem pencernaan dan endokrin','menghasilkan enzim pencernaan serta hormon seperti insulin'),('Limpa','sistem limfatik','menyaring darah dan mendukung respons imun'),('Kulit','sistem integumen','melindungi tubuh dan membantu pengaturan suhu'),('Tulang','sistem rangka','menopang tubuh, melindungi organ, dan menyimpan mineral'),('Otot rangka','sistem muskuloskeletal','menghasilkan gerakan sadar dengan menarik tulang'),('Diafragma','sistem pernapasan','menjadi otot utama yang membantu menarik udara ke paru-paru'),('Tiroid','sistem endokrin','menghasilkan hormon yang mengatur metabolisme'),('Kandung kemih','sistem urinaria','menyimpan urine sebelum dikeluarkan'),('Mata','sistem sensorik','mengubah cahaya menjadi sinyal saraf untuk penglihatan'),('Telinga dalam','sistem sensorik','berperan dalam pendengaran dan keseimbangan'),('Sumsum tulang','sistem hematopoietik','menghasilkan sebagian besar sel darah')]
for name,system,function in organs:
    add('Tubuh Manusia',f'{name} merupakan bagian {system}.',f'Dalam anatomi manusia, {name} berhubungan terutama dengan {system}.',nih,nih_url)
    add('Tubuh Manusia',f'Fungsi utama {name}.',f'{name} {function}.',nih,nih_url)

smith='Smithsonian Ocean & Natural History'; smith_url='https://ocean.si.edu/ocean-life'
animals=[
('Gurita','moluska','memiliki tiga jantung dan darah berbasis hemosianin'),('Lumba-lumba','mamalia laut','bernapas dengan paru-paru melalui lubang sembur'),('Paus biru','mamalia laut','merupakan hewan terbesar yang diketahui'),('Kelelawar','mamalia','mampu melakukan penerbangan aktif berkelanjutan'),('Platipus','mamalia monotremata','bertelur meskipun termasuk mamalia'),('Echidna','mamalia monotremata','juga berkembang biak dengan bertelur'),('Burung','vertebrata','merupakan keturunan dinosaurus theropoda'),('Hiu','ikan bertulang rawan','memiliki kerangka terutama dari tulang rawan'),('Pari','ikan bertulang rawan','berkerabat dekat dengan hiu'),('Kuda laut','ikan','mengerami embrio di kantong tubuh pejantan'),('Axolotl','amfibi','mampu meregenerasi anggota tubuh dan beberapa jaringan'),('Bintang laut','echinodermata','bukan ikan dan tidak memiliki tulang belakang'),('Ubur-ubur','cnidaria','menggunakan jaringan saraf tanpa otak terpusat'),('Lebah','serangga','dapat melihat pola ultraviolet pada bunga'),('Semut','serangga','banyak berkomunikasi menggunakan feromon'),('Rayap','serangga','secara evolusioner berada dalam garis keturunan kecoak'),('Laba-laba','arachnida','memiliki delapan kaki sehingga bukan serangga'),('Kupu-kupu','serangga','memiliki reseptor pengecap pada kaki'),('Bunglon','reptil','mengubah warna untuk komunikasi, suhu, stres, dan kamuflase'),('Penguin','burung','menggunakan sayap yang termodifikasi sebagai sirip'),('Beruang kutub','mamalia','memiliki kulit gelap di bawah bulunya'),('Gajah','mamalia','dapat berkomunikasi dengan panggilan infrasonik'),('Koala','mamalia marsupial','memiliki pola sidik jari yang mirip primata'),('Karang','hewan cnidaria','membentuk koloni polip yang menghasilkan rangka kapur'),('Spons laut','hewan porifera','termasuk garis keturunan hewan yang sangat awal')]
for name,group,feature in animals:
    add('Zoologi',f'{name} termasuk {group}.',f'Secara taksonomi, {name} ditempatkan dalam kelompok {group}.',smith,smith_url)
    add('Zoologi',f'Keunikan {name}.',f'{name} {feature}.',smith,smith_url)

usgs='USGS & NOAA'; earth_url='https://www.usgs.gov/programs/earthquake-hazards/science-earthquakes'; ocean_url='https://oceanexplorer.noaa.gov/ocean-fact/climate/'
earth=[
('Usia Bumi','Bumi berusia sekitar 4,54 miliar tahun','penanggalan radiometrik meteorit dan batuan tertua menjadi dasar estimasi ini',earth_url),('Lempeng tektonik','litosfer Bumi terbagi menjadi lempeng yang bergerak perlahan','banyak gempa dan gunung api terkonsentrasi di batas lempeng',earth_url),('Hiposenter','hiposenter adalah titik awal gempa di bawah permukaan','episenter adalah titik di permukaan tepat di atasnya',earth_url),('Gempa susulan','gempa utama biasanya diikuti gempa susulan','susulan dapat berlangsung berminggu-minggu hingga bertahun-tahun',earth_url),('Prediksi gempa','gempa tertentu belum dapat diprediksi tepat waktu, lokasi, dan magnitudonya','ilmuwan dapat membuat peta bahaya dan estimasi probabilitas',earth_url),('Gelombang P','gelombang primer adalah gelombang seismik tercepat','karena itu gelombang P biasanya tercatat lebih dahulu',earth_url),('Magnitudo gempa','magnitudo menyatakan ukuran sumber gempa','intensitas menggambarkan kekuatan guncangan di lokasi tertentu',earth_url),('Magma dan lava','batuan cair di bawah permukaan disebut magma','setelah keluar ke permukaan material cair itu disebut lava',earth_url),('Inti Bumi','inti luar Bumi bersifat cair','inti dalam tetap padat akibat tekanan yang sangat tinggi',earth_url),('Medan magnet','gerakan logam cair di inti luar membantu membangkitkan medan magnet','kutub magnet Bumi bergerak dan pernah berbalik',earth_url),('Atmosfer','atmosfer kering Bumi terutama terdiri dari nitrogen','oksigen mencakup sekitar seperlima atmosfer kering',earth_url),('Troposfer','troposfer adalah lapisan atmosfer terbawah','sebagian besar cuaca berlangsung di lapisan ini',earth_url),('Ozon stratosfer','ozon stratosfer menyerap banyak radiasi ultraviolet','lapisan ini membantu melindungi kehidupan di permukaan',earth_url),('Gurun','gurun ditentukan terutama oleh curah hujan rendah','karena itu gurun dapat bersuhu panas maupun dingin',earth_url),('Antarktika','pedalaman Antarktika menerima sangat sedikit presipitasi','wilayah ini diklasifikasikan sebagai gurun kutub',earth_url),('Luas samudra','samudra menutupi sekitar 71 persen permukaan Bumi','samudra membentuk satu badan air global yang saling terhubung',ocean_url),('Air laut','sekitar 97 persen air Bumi berada di samudra','air tersebut mengandung garam terlarut sehingga tidak langsung dapat diminum',ocean_url),('Iklim laut','laut menyimpan radiasi Matahari dalam jumlah besar','arus laut lalu membantu memindahkan panas di seluruh planet',ocean_url),('Hujan daratan','hampir seluruh hujan daratan bermula dari penguapan laut','uap air dipindahkan atmosfer sebelum mengembun dan jatuh',ocean_url),('Arus laut','arus digerakkan angin, perbedaan kerapatan, rotasi Bumi, dan pasang','arus membantu menyeimbangkan distribusi panas global',ocean_url),('Pasang laut','gravitasi Bulan memberi pengaruh utama pada pasang','gravitasi Matahari juga memberikan kontribusi',ocean_url),('Tekanan laut','tekanan air bertambah seiring kedalaman','peningkatan berasal dari berat kolom air di atasnya',ocean_url),('Zona fotik','zona fotik menerima cukup cahaya untuk fotosintesis','fitoplankton hidup dan menjadi produsen penting di lapisan ini',ocean_url),('Ventilasi hidrotermal','ekosistem ventilasi laut dalam tidak bergantung langsung pada cahaya','mikroba kemosintetik menjadi dasar rantai makanannya',ocean_url),('Pengasaman laut','karbon dioksida terlarut membentuk asam karbonat','proses ini menurunkan pH laut dan memengaruhi organisme pembentuk cangkang',ocean_url)]
for topic,a,b,url in earth:
    add('Ilmu Bumi & Laut',topic+'.',a.capitalize()+'.',usgs,url)
    add('Ilmu Bumi & Laut','Penjelasan '+topic.lower()+'.',b.capitalize()+'.',usgs,url)

assert len(facts)==300, len(facts)
DATA.write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Generated {len(facts)} facts and upgraded {INDEX}')

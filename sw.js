const CACHE_NAME = 'naturalai-v1';
const ASSETS = [
  '/natural-ai/',
  '/natural-ai/index.html',
  '/natural-ai/manifest.json',
  '/natural-ai/logo.jpeg',
  '/natural-ai/safe_drink.png',
  '/natural-ai/spiked_drink.png',
  '/natural-ai/water_glass.png',
  '/natural-ai/cola_glass.png',
  '/natural-ai/cocktail_glass.png',
  '/natural-ai/blueberry_smoothie.png',
  '/natural-ai/berry_oatmeal.png',
  '/natural-ai/grilled_chicken.png',
  '/natural-ai/avocado_toast.png',
  '/natural-ai/baked_salmon.png',
  '/natural-ai/caesar_salad.png',
  '/natural-ai/banana_pancakes.png',
  '/natural-ai/greek_yogurt_bowl.png',
  '/natural-ai/quinoa_power_bowl.png',
  '/natural-ai/veggie_stir_fry.png',
  '/natural-ai/meal_0.png',
  '/natural-ai/audio/scan.wav',
  '/natural-ai/audio/success.wav'
];

// Install — cache all assets
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch — serve from cache, fallback to network
self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});

// Simple common utilities used by pages
window.AsyncStorage = {
  async set(key,val){ return new Promise(res=>{ localStorage.setItem(key, JSON.stringify(val)); res(true); }); },
  async get(key){ return new Promise(res=>{ const v = localStorage.getItem(key); res(v?JSON.parse(v):null); }); },
  async remove(key){ return new Promise(res=>{ localStorage.removeItem(key); res(true); }); }
};

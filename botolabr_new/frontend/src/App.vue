<template>
  <link rel="stylesheet" href="https://fonts-online.ru/css/lobelia">
  <link rel="stylesheet" href="https://fonts-online.ru/css/nauryzredkeds">
  <link rel="stylesheet" href="https://fonts-online.ru/css/gogol">
  
  <router-view />
</template>

<script setup>
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --pink-dark:   #FB6E17;
  --green-light: #ADF36C;
  --green-dark:  #0B5000;
  --bg:          #FEDAEC;
  --surface:     #FB9250;
  --surface2:    #FDA36C;
  --border:      #FB6E17;
  --text:        #F6FEDE;
  --text-muted:  #ADF36C;
  --red:         #ef4444;
  --blue:        #3b82f6;
  --purple:      #a855f7;
  --radius:      12px;
  --shadow:      0 4px 24px rgba(0,0,0,.4);
}

body {
  font-family: 'Roboto slab', system-ui, sans-serif;
  background: var(--text);
  color: var(--text);
  min-height: 100vh;
}

a { color: 'Roboto slab'; text-decoration: none; }

button {
  cursor: pointer;
  font-family: 'Roboto slab';
  border: none;
  outline: none;
}

input, textarea, select {
  font-family: 'Roboto slab';
  outline: none;
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--pink-dark);
  border-radius: 8px;
  padding: 10px 14px;
  width: 100%;
  font-size: clamp(12px, 2vw, 16px);
  transition: border-color .2s;
}
input:focus, textarea:focus, select:focus {
  border-color: var(--text);
}
input::placeholder, textarea::placeholder { color: var(--pink-dark); }

/* ── Scrollbar ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Toast ─────────────────────────────────────────────────────────────── */
.toast-wrap {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 9999;
}
.toast {
  padding: 12px 18px;
  border-radius: 8px;
  font-size: clamp(12px, 2vw, 16px);
  font-weight: 500;
  animation: toastIn .25s ease;
  max-width: 320px;
}
.toast.success { background: var(--green);  color: #fff; }
.toast.error   { background: var(--red);    color: #fff; }
.toast.info    { background: var(--surface2); color: var(--text); border: 1px solid var(--border); }
@keyframes toastIn {
  from { transform: translateX(40px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

/* ── Modal ─────────────────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn .15s ease;
}
.modal {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 28px 32px;
  width: 100%; max-width: 440px;
  animation: slideUp .2s ease;
}

.modal h3 { font-size: clamp(18px, 2vw, 22px); font-family: 'NauryzRedKeds'; margin-bottom: 20px; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; }
@keyframes fadeIn  { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

/* ── Buttons ───────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 10px 18px; border-radius: 8px;
  font-size: clamp(12px, 2vw, 16px);
  font-weight: 500;
  transition: all .18s;
}
.btn-primary   { background: var(--green-dark);  color: #F6FEDE; }
.btn-primary:hover  { background: var(--green-light); }
.btn-secondary { background: var(--green-dark); color: var(--text); }
.btn-secondary:hover { background: var(--green-light); }
.btn-danger    { background: var(--red);   color: #fff; }
.btn-danger:hover { opacity: .85; }
.btn-ghost     { background: transparent; color: var(--green-dark); }
.btn-ghost:hover { color: var(--text); }
.btn:disabled  { opacity: .5; cursor: not-allowed; }
.btn-sm        { padding: 6px 12px; font-size: clamp(12px, 2vw, 16px); }

/* ── Form group ────────────────────────────────────────────────────────── */
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: clamp(12px, 2vw, 16px); color: var(--text); margin-bottom: 6px; }

/* ── Card ──────────────────────────────────────────────────────────────── */
.card {
  background: linear-gradient(135deg, var(--green-dark) 10%, var(--green-light) 100%);;
  border: 1px solid var(--green-light);
  border-radius: var(--radius);
  padding: 20px;
}

/* ── Badge ─────────────────────────────────────────────────────────────── */
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 2px 8px; border-radius: 20px;
  font-size: 11px; font-weight: 600;
}
.badge-green  { background: rgba(22,101,52,.3);  color: var(--green-light); }
.badge-red    { background: rgba(239,68,68,.2);  color: #fca5a5; }
.badge-gray   { background: var(--green-dark);     color: var(--text-muted); }
</style>

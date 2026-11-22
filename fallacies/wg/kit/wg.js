/* Well & Good interface kit, the script. Load it in <head>, after wg.css, with no defer:
     <script src="…/kit/wg.js"></script>
   It sets the mode before the page draws, then wires the controls once the page has loaded.

   What it does
   - Mode: reads the saved choice (localStorage "wg-mode", dark when none) and sets data-mode on <html>.
     Any button with data-wg-mode switches it. Inside the button, an element with data-wg-mode-label
     gets the text and one with data-wg-mode-icon gets the sun or the moon.
   - Icons: an empty element with data-wg-icon="name" gets that icon.
   - Logo: an empty element with data-wg-logo="wordmark", "ampersand" or "stacked" gets that logo.
   - Tabs: a container with data-wg-tabs holds [role=tab] buttons with aria-controls.
   - Pressed groups: a container with data-wg-pick keeps one of its [aria-pressed] buttons pressed.
   - Menus: a <details class="wg-menu"> closes on Escape and on a click outside it.
   - Dialogs: data-wg-open="id" opens a <dialog>, data-wg-close closes the one it sits in.
   - Navigation on small screens: data-wg-toggle="id" opens and closes that element (class is-open).
   - Toasts: WG.toast("Saved").
   The page hears about a mode change through the "wg:mode" event on document. */

(function () {
  const root = document.documentElement;
  const KEY = "wg-mode";

  let saved = "dark";
  try { saved = localStorage.getItem(KEY) || "dark"; } catch {}
  root.dataset.mode = saved === "light" ? "light" : "dark";

  /* line icons on a 24 unit box, drawn in the current text color. The paths are from Lucide (ISC license);
     Well & Good has not chosen its own icon set yet. */
  const ICONS = {
    assets: '<rect x="3" y="3" width="18" height="18"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
    colors: '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    pairings: '<circle cx="12" cy="12" r="10"/><path d="M12 18a6 6 0 0 0 0-12v12z"/>',
    type: '<path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>',
    spacing: '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
    components: '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 12 10 5 10-5"/><path d="m2 17 10 5 10-5"/>',
    icons: '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>',
    motion: '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    voice: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    access: '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    ai: '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    server: '<rect x="2" y="2" width="20" height="8"/><rect x="2" y="14" width="20" height="8"/><path d="M6 6h.01"/><path d="M6 18h.01"/>',
    search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    moon: '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/>',
    download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    folder: '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.7-.9l-.8-1.2A2 2 0 0 0 7.9 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2z"/>',
    file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
    arrow: '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    back: '<path d="M19 12H5"/><path d="m11 18-6-6 6-6"/>',
    down: '<path d="m6 9 6 6 6-6"/>',
    up: '<path d="m18 15-6-6-6 6"/>',
    close: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    check: '<path d="M20 6 9 17l-5-5"/>',
    plus: '<path d="M12 5v14"/><path d="M5 12h14"/>',
    minus: '<path d="M5 12h14"/>',
    info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    warn: '<path d="m21.7 18-8-14a2 2 0 0 0-3.4 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    error: '<path d="M7.9 2h8.2L22 7.9v8.2L16.1 22H7.9L2 16.1V7.9z"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    ok: '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    user: '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
    settings: '<path d="M20 7h-9"/><path d="M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/>',
    home: '<path d="M3 10 12 3l9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    calendar: '<rect x="3" y="4" width="18" height="18"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    filter: '<path d="M22 3H2l8 9.5V19l4 2v-8.5z"/>',
    mail: '<rect x="2" y="4" width="20" height="16"/><path d="m22 7-10 6L2 7"/>',
    lock: '<rect x="3" y="11" width="18" height="11"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    link: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    copy: '<rect x="9" y="9" width="13" height="13"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    trash: '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    chart: '<path d="M3 3v18h18"/><path d="M8 17V9"/><path d="M13 17V5"/><path d="M18 17v-6"/>',
    inbox: '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5.1 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.5-6.9A2 2 0 0 0 16.8 4H7.2a2 2 0 0 0-1.7 1.1z"/>',
    menu: '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    more: '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
    play: '<path d="m6 3 14 9-14 9z"/>',
    clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    book: '<path d="M4 19.5V5a2 2 0 0 1 2-2h14v18H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
    out: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
  };
  const icon = (name, extra) =>
    `<svg class="wg-icon${extra ? " " + extra : ""}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">${ICONS[name] || ""}</svg>`;

  /* the three logo files, drawn in the current text color */
  const LOGOS = {"wordmark": "<svg fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1559.38 356.76\"><g><path d=\"M990.94,86.23h61.43c-1.48,19.24-2.22,38.86-2.22,58.84v121.02c0,51.44-16.65,90.67-76.98,90.67-45.52,0-68.1-25.91-68.1-66.99h48.85c0,12.21,5.18,23.69,18.5,23.69,11.47,0,18.5-6.29,18.5-29.24v-69.58c-5.18,35.16-22.58,52.92-41.45,52.92-33.31,0-52.55-38.86-52.55-86.23,0-59.95,21.09-99.92,55.51-99.92,25.17,0,34.42,29.98,38.49,59.21v-54.4ZM990.94,167.28c0-15.91-3.7-35.9-16.28-35.9-14.8,0-19.24,19.25-19.24,45.52,0,28.5,5.92,49.22,17.76,49.22,9.99,0,17.76-11.84,17.76-41.82v-17.02Z\"/><path d=\"M1224.09,180.6c0,59.95-24.79,99.18-76.24,99.18s-76.61-39.23-76.61-99.18,25.17-99.18,76.61-99.18,76.24,39.23,76.24,99.18ZM1130.09,180.6c0,31.83,5.18,53.66,17.76,53.66s17.39-21.83,17.39-53.66-4.44-53.66-17.39-53.66-17.76,21.83-17.76,53.66Z\"/><path d=\"M1388.78,180.6c0,59.95-24.79,99.18-76.24,99.18s-76.61-39.23-76.61-99.18,25.17-99.18,76.61-99.18,76.24,39.23,76.24,99.18ZM1294.77,180.6c0,31.83,5.18,53.66,17.76,53.66s17.39-21.83,17.39-53.66-4.44-53.66-17.39-53.66-17.76,21.83-17.76,53.66Z\"/><path d=\"M1498.32,141.74V0h59.21v214.65c0,19.98.74,41.45,1.85,60.69h-61.06v-56.25c-3.33,24.06-16.65,60.69-42.56,60.69-35.16,0-51.44-38.86-51.44-105.84,0-45.89,14.8-92.52,48.85-92.52,22.95,0,37.75,21.47,45.15,60.32ZM1463.16,179.12c0,34.42,6.66,50.7,20.36,50.7,6.66,0,15.17-9.25,15.17-41.45v-11.84c0-28.5-6.66-43.67-18.5-43.67s-17.02,15.91-17.02,46.26Z\"/><path d=\"M64.02,86.23l6.66,76.98c1.85,20.72,3.7,38.86,5.18,55.88h1.11c2.59-17.02,5.92-37.01,9.62-55.14l14.43-77.72h45.89l13.69,76.24c3.7,21.46,7.03,39.6,8.88,56.62h.74c1.11-16.65,2.59-36.64,5.18-56.62l8.51-76.24h58.84l-49.22,189.12h-51.07l-10.73-55.14c-3.33-16.65-7.4-38.12-9.25-59.95h-.74c-2.22,21.84-6.29,42.56-10.73,59.95l-13.32,55.14h-51.07L0,86.23h64.02Z\"/><path d=\"M388.96,190.6h-87.34c.74,10.36,1.85,19.24,3.33,26.65,2.96,10.73,7.77,17.02,14.43,17.02,8.88,0,12.95-8.51,14.06-25.54h56.25c-5.18,45.15-27.39,71.06-70.32,71.06-51.44,0-76.61-39.23-76.61-99.18s25.17-99.18,76.61-99.18,71.43,36.64,71.43,84.75c0,8.14-.74,19.61-1.85,24.43ZM302.73,156.55h31.09c-1.48-18.5-5.55-29.61-14.43-29.61-9.62,0-14.43,11.47-16.65,29.61Z\"/><path d=\"M413.01,0h59.58v275.35h-59.58V0Z\"/><path d=\"M500.35,0h59.58v275.35h-59.58V0Z\"/><path d=\"M846.13,122.46c-10.16,31.54-23.83,74.65-47.67,107.25l40.31,47.67h-68.69l-9.46-11.22c-15.07,9.11-32.24,14.02-52.57,14.02-63.79,0-88.32-36.45-88.32-71.5,0-47.31,34.7-68.69,73.6-84.46-28.74.35-48.02-17.17-48.02-41.36,0-30.14,22.08-53.97,69.75-53.97,43.11,0,64.14,24.18,64.49,53.27.7,26.64-9.46,48.37-53.97,71.5-29.79,15.07-47.67,29.09-47.67,50.82,0,15.07,10.51,29.44,32.59,29.44,44.16,0,66.24-51.52,84.11-111.45h51.52ZM708.39,116.15c11.57-6.66,17.52-15.42,17.52-29.79,0-8.41-3.15-18.58-14.02-18.58s-16.82,9.11-16.82,22.43c0,10.16,5.26,22.43,13.32,25.94Z\"/></g></svg>", "ampersand": "<svg fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 341.86 379.43\"><g><path d=\"M341.86,141.29c-15.35,47.63-35.98,112.72-71.97,161.93l60.86,71.97h-103.72l-14.29-16.93c-22.75,13.76-48.69,21.17-79.38,21.17C37.04,379.43,0,324.39,0,271.47c0-71.44,52.39-103.72,111.13-127.54-43.39.53-72.5-25.93-72.5-62.44C38.63,35.98,71.97,0,143.94,0c65.09,0,96.84,36.51,97.37,80.44,1.06,40.22-14.29,73.03-81.5,107.96-44.98,22.75-71.97,43.92-71.97,76.73,0,22.75,15.88,44.45,49.21,44.45,66.68,0,100.02-77.79,127.01-168.28h77.79ZM133.89,131.77c17.46-10.05,26.46-23.29,26.46-44.98,0-12.7-4.76-28.05-21.17-28.05s-25.4,13.76-25.4,33.87c0,15.35,7.94,33.87,20.11,39.16Z\"/></g></svg>", "stacked": "<svg fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1065.96 766.4\"><g><path d=\"M67.38,201.44l6.66,76.98c1.85,20.72,3.7,38.86,5.18,55.88h1.11c2.59-17.02,5.92-37.01,9.62-55.14l14.43-77.72h45.89l13.69,76.24c3.7,21.46,7.03,39.6,8.88,56.62h.74c1.11-16.65,2.59-36.64,5.18-56.62l8.51-76.24h58.84l-49.22,189.11h-51.07l-10.73-55.14c-3.33-16.65-7.4-38.12-9.25-59.95h-.74c-2.22,21.84-6.29,42.56-10.73,59.95l-13.32,55.14h-51.07L3.36,201.44h64.02Z\"/><path d=\"M392.32,305.8h-87.34c.74,10.36,1.85,19.24,3.33,26.65,2.96,10.73,7.77,17.02,14.43,17.02,8.88,0,12.95-8.51,14.06-25.54h56.25c-5.18,45.15-27.39,71.06-70.32,71.06-51.44,0-76.61-39.23-76.61-99.18s25.17-99.18,76.61-99.18,71.43,36.64,71.43,84.75c0,8.14-.74,19.61-1.85,24.43ZM306.09,271.75h31.09c-1.48-18.5-5.55-29.61-14.43-29.61-9.62,0-14.43,11.47-16.65,29.61Z\"/><path d=\"M416.37,115.21h59.58v275.34h-59.58V115.21Z\"/><path d=\"M503.71,115.21h59.58v275.34h-59.58V115.21Z\"/><path d=\"M47.5,71.63V0h29.92v108.48c0,10.1.37,20.95.94,30.67h-30.86v-28.43c-1.68,12.16-8.42,30.67-21.51,30.67-17.77,0-26-19.64-26-53.49,0-23.19,7.48-46.76,24.69-46.76,11.6,0,19.08,10.85,22.82,30.49ZM29.74,90.52c0,17.39,3.37,25.62,10.29,25.62,3.37,0,7.67-4.68,7.67-20.95v-5.98c0-14.4-3.37-22.07-9.35-22.07s-8.6,8.04-8.6,23.38Z\"/><path d=\"M163.27,91.27c0,30.3-12.53,50.12-38.53,50.12s-38.71-19.82-38.71-50.12,12.72-50.12,38.71-50.12,38.53,19.83,38.53,50.12ZM115.77,91.27c0,16.08,2.62,27.12,8.98,27.12s8.79-11.03,8.79-27.12-2.24-27.12-8.79-27.12-8.98,11.04-8.98,27.12Z\"/><path d=\"M174.67,10.66h30.11v24.31h-30.11V10.66ZM174.67,43.58h30.11v95.57h-30.11V43.58Z\"/><path d=\"M296.05,79.11v60.04h-30.11v-57.23c0-7.85-1.68-14.59-7.67-14.59-6.92,0-9.16,8.04-9.16,16.65v55.17h-30.11v-65.08c0-10.1-.37-20.76-.75-30.49h30.86v29.36c2.06-15.71,8.98-31.61,23.19-31.61,18.52,0,23.75,15.34,23.75,37.78Z\"/><path d=\"M354.03,43.58h31.05c-.75,9.73-1.12,19.64-1.12,29.74v61.16c0,26-8.42,45.82-38.9,45.82-23,0-34.41-13.09-34.41-33.85h24.69c0,6.17,2.62,11.97,9.35,11.97,5.8,0,9.35-3.18,9.35-14.77v-35.16c-2.62,17.77-11.41,26.74-20.95,26.74-16.83,0-26.56-19.64-26.56-43.58,0-30.3,10.66-50.5,28.05-50.5,12.72,0,17.39,15.15,19.45,29.92v-27.49ZM354.03,84.54c0-8.04-1.87-18.14-8.23-18.14-7.48,0-9.73,9.72-9.73,23,0,14.4,2.99,24.88,8.98,24.88,5.05,0,8.98-5.99,8.98-21.13v-8.6Z\"/><path d=\"M920.51,149.31c-14.16,43.95-33.21,104.02-66.42,149.44l56.16,66.42h-95.72l-13.19-15.63c-21,12.7-44.93,19.54-73.26,19.54-88.88,0-123.07-50.79-123.07-99.63,0-65.93,48.35-95.72,102.56-117.7-40.05.49-66.91-23.93-66.91-57.63,0-42,30.77-75.21,97.19-75.21,60.07,0,89.37,33.7,89.86,74.23.98,37.12-13.19,67.4-75.21,99.63-41.51,21-66.42,40.53-66.42,70.81,0,21,14.65,41.02,45.42,41.02,61.54,0,92.3-71.79,117.21-155.3h71.79ZM728.58,140.52c16.12-9.28,24.42-21.49,24.42-41.51,0-11.72-4.4-25.88-19.53-25.88s-23.44,12.7-23.44,31.26c0,14.16,7.33,31.26,18.56,36.14Z\"/><path d=\"M497.51,413.04h61.43c-1.48,19.24-2.22,38.86-2.22,58.84v121.02c0,51.44-16.65,90.67-76.98,90.67-45.52,0-68.1-25.91-68.1-66.99h48.85c0,12.21,5.18,23.69,18.5,23.69,11.47,0,18.5-6.29,18.5-29.24v-69.58c-5.18,35.16-22.58,52.92-41.45,52.92-33.31,0-52.55-38.86-52.55-86.23,0-59.95,21.09-99.92,55.51-99.92,25.17,0,34.42,29.98,38.49,59.21v-54.4ZM497.51,494.08c0-15.91-3.7-35.9-16.28-35.9-14.8,0-19.24,19.25-19.24,45.52,0,28.5,5.92,49.22,17.76,49.22,9.99,0,17.76-11.84,17.76-41.82v-17.02Z\"/><path d=\"M730.67,507.41c0,59.95-24.79,99.18-76.24,99.18s-76.61-39.23-76.61-99.18,25.17-99.18,76.61-99.18,76.24,39.23,76.24,99.18ZM636.66,507.41c0,31.83,5.18,53.66,17.76,53.66s17.39-21.83,17.39-53.66-4.44-53.66-17.39-53.66-17.76,21.83-17.76,53.66Z\"/><path d=\"M895.35,507.41c0,59.95-24.79,99.18-76.24,99.18s-76.61-39.23-76.61-99.18,25.17-99.18,76.61-99.18,76.24,39.23,76.24,99.18ZM801.35,507.41c0,31.83,5.18,53.66,17.76,53.66s17.39-21.83,17.39-53.66-4.44-53.66-17.39-53.66-17.76,21.83-17.76,53.66Z\"/><path d=\"M1004.89,468.55v-141.74h59.21v214.65c0,19.98.74,41.45,1.85,60.69h-61.06v-56.25c-3.33,24.06-16.65,60.69-42.56,60.69-35.16,0-51.44-38.86-51.44-105.84,0-45.89,14.8-92.52,48.85-92.52,22.95,0,37.75,21.47,45.15,60.32ZM969.73,505.93c0,34.42,6.66,50.7,20.36,50.7,6.66,0,15.17-9.25,15.17-41.45v-11.84c0-28.5-6.66-43.67-18.5-43.67s-17.02,15.91-17.02,46.26Z\"/><path d=\"M753.02,721.93c0,26.88-11.12,44.47-34.18,44.47s-34.35-17.59-34.35-44.47,11.28-44.47,34.35-44.47,34.18,17.59,34.18,44.47ZM710.88,721.93c0,14.27,2.32,24.06,7.96,24.06s7.8-9.79,7.8-24.06-1.99-24.06-7.8-24.06-7.96,9.79-7.96,24.06Z\"/><path d=\"M830.67,711.15v53.26h-26.71v-50.77c0-6.97-1.49-12.94-6.8-12.94-6.14,0-8.13,7.13-8.13,14.77v48.95h-26.71v-57.74c0-8.96-.33-18.42-.66-27.05h27.38v26.05c1.83-13.94,7.96-28.04,20.57-28.04,16.43,0,21.07,13.61,21.07,33.52Z\"/><path d=\"M841.62,640.96h26.71v123.45h-26.71v-123.45Z\"/><path d=\"M880.45,650.42h26.71v21.57h-26.71v-21.57ZM880.45,679.62h26.71v84.79h-26.71v-84.79Z\"/><path d=\"M988.13,711.15v53.26h-26.71v-50.77c0-6.97-1.49-12.94-6.8-12.94-6.14,0-8.13,7.13-8.13,14.77v48.95h-26.71v-57.74c0-8.96-.33-18.42-.66-27.05h27.38v26.05c1.83-13.94,7.96-28.04,20.57-28.04,16.43,0,21.07,13.61,21.07,33.52Z\"/><path d=\"M1061.47,726.41h-39.16c.33,4.65.83,8.63,1.49,11.95,1.33,4.81,3.48,7.63,6.47,7.63,3.98,0,5.81-3.82,6.31-11.45h25.22c-2.32,20.24-12.28,31.86-31.53,31.86-23.06,0-34.35-17.59-34.35-44.47s11.28-44.47,34.35-44.47,32.02,16.43,32.02,38c0,3.65-.33,8.79-.83,10.95ZM1022.81,711.15h13.94c-.66-8.3-2.49-13.27-6.47-13.27-4.31,0-6.47,5.14-7.47,13.27Z\"/></g></svg>"};

  function paintMode() {
    const now = root.dataset.mode;
    const other = now === "dark" ? "light" : "dark";
    const say = `Switch to ${other} mode`;
    document.querySelectorAll("[data-wg-mode]").forEach((b) => {
      const label = b.querySelector("[data-wg-mode-label]");
      const sign = b.querySelector("[data-wg-mode-icon]");
      if (label) label.textContent = other[0].toUpperCase() + other.slice(1) + " mode";
      if (sign) sign.innerHTML = icon(other === "light" ? "sun" : "moon");
      if (!label && !sign && !b.children.length) b.innerHTML = icon(other === "light" ? "sun" : "moon");
      b.title = say;
      if (!label) b.setAttribute("aria-label", say);
    });
  }

  function setMode(next) {
    root.dataset.mode = next === "light" ? "light" : "dark";
    try { localStorage.setItem(KEY, root.dataset.mode); } catch {}
    paintMode();
    document.dispatchEvent(new CustomEvent("wg:mode", { detail: root.dataset.mode }));
  }

  function fillIcons(scope) {
    (scope || document).querySelectorAll("[data-wg-icon]").forEach((el) => {
      if (!el.firstElementChild) el.innerHTML = icon(el.dataset.wgIcon);
    });
    (scope || document).querySelectorAll("[data-wg-logo]").forEach((el) => {
      if (!el.firstElementChild) el.innerHTML = LOGOS[el.dataset.wgLogo] || "";
    });
  }

  function toast(text, ms) {
    let box = document.querySelector(".wg-toasts");
    if (!box) {
      box = document.createElement("div");
      box.className = "wg-toasts"; box.setAttribute("role", "status"); box.setAttribute("aria-live", "polite");
      document.body.append(box);
    }
    const t = document.createElement("div");
    t.className = "wg-toast";
    const words = document.createElement("span"); words.textContent = text;
    const shut = document.createElement("button"); shut.type = "button"; shut.setAttribute("aria-label", "Dismiss"); shut.textContent = "×";
    shut.addEventListener("click", () => t.remove());
    t.append(words, shut); box.append(t);
    setTimeout(() => t.remove(), ms || 5000);
  }

  function selectTab(tab) {
    const list = tab.closest("[data-wg-tabs]");
    list.querySelectorAll('[role="tab"]').forEach((t) => {
      const on = t === tab;
      t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1;
      const panel = document.getElementById(t.getAttribute("aria-controls"));
      if (panel) panel.hidden = !on;
    });
  }

  /* every control is found at the moment of the click, so markup added later works too */
  document.addEventListener("click", (e) => {
    const at = (sel) => e.target.closest(sel);
    if (at("[data-wg-mode]")) return setMode(root.dataset.mode === "dark" ? "light" : "dark");
    const tab = at('[data-wg-tabs] [role="tab"]');
    if (tab) return selectTab(tab);
    const pick = at("[data-wg-pick] [aria-pressed]");
    if (pick) pick.closest("[data-wg-pick]").querySelectorAll("[aria-pressed]").forEach((b) => b.setAttribute("aria-pressed", String(b === pick)));
    const toggle = at("[data-wg-toggle]");
    if (toggle) {
      const target = document.getElementById(toggle.dataset.wgToggle);
      if (target) toggle.setAttribute("aria-expanded", String(target.classList.toggle("is-open")));
    }
    const opener = at("[data-wg-open]");
    if (opener) document.getElementById(opener.dataset.wgOpen)?.showModal();
    const closer = at("[data-wg-close]");
    if (closer) closer.closest("dialog")?.close();
    document.querySelectorAll("details.wg-menu[open]").forEach((m) => { if (!m.contains(e.target)) m.open = false; });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") document.querySelectorAll("details.wg-menu[open]").forEach((m) => { m.open = false; m.querySelector("summary")?.focus(); });
    const tab = e.target.closest?.('[data-wg-tabs] [role="tab"]');
    const step = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
    if (tab && step) {
      const tabs = [...tab.closest("[data-wg-tabs]").querySelectorAll('[role="tab"]')];
      const next = tabs[(tabs.indexOf(tab) + step + tabs.length) % tabs.length];
      next.focus(); selectTab(next);
    }
  });

  function start() {
    fillIcons(); paintMode();
    document.querySelectorAll('[data-wg-tabs] [role="tab"][aria-selected="true"]').forEach(selectTab);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();

  window.WG = { setMode, mode: () => root.dataset.mode, icon, icons: Object.keys(ICONS), logos: LOGOS, fillIcons, paintMode, toast };
})();

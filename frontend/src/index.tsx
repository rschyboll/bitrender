import PrimeReact from 'primereact/api';
import ReactDOMClient from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';

import { App } from '@/app';
import '@/scss/global.scss';

import './i18n';

PrimeReact.ripple = true;

function Init() {
  return (
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
}

ReactDOMClient.createRoot(document.getElementById('app') as HTMLElement).render(
  <Init />,
);

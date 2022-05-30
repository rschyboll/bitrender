import { Provider as InversifyProvider } from 'inversify-react';
import PrimeReact from 'primereact/api';
import ReactDOMClient from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';

import { App } from '@/app';
import '@/scss/global.scss';
import '@/scss/main.scss';

import { DepContainer } from './deps';
import './i18n';
import './logic';

PrimeReact.ripple = true;

function Init() {
  return (
    <InversifyProvider container={DepContainer}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </InversifyProvider>
  );
}

ReactDOMClient.createRoot(document.getElementById('app') as HTMLElement).render(
  <Init />,
);

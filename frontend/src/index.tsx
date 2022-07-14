import { Provider as InversifyProvider } from 'inversify-react';
import PrimeReact from 'primereact/api';
import { useEffect } from 'react';
import ReactDOMClient from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';

import { App } from '@/app';
import { startGlobalLogics, startKea } from '@/logic';
import '@/scss/global.scss';
import '@/scss/main.scss';

import Dependencies from './deps';
import './i18n';
import './logic';

PrimeReact.ripple = true;

startKea();

function Init() {
  useEffect(() => {
    startGlobalLogics();
  }, []);

  return (
    <InversifyProvider container={Dependencies}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </InversifyProvider>
  );
}

ReactDOMClient.createRoot(document.getElementById('app') as HTMLElement).render(
  <Init />,
);

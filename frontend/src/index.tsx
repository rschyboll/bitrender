import { Provider as InversifyProvider } from 'inversify-react';
import PrimeReact from 'primereact/api';
import { useEffect } from 'react';
import { createRoot } from 'react-dom/client';

import { App } from '@/app';
import { startGlobalLogics, startKea } from '@/logic';
import '@/scss/global.scss';
import '@/scss/main.scss';

import Dependencies from './deps';
import './i18n';
import './logic';
import { HistoryRouter } from './route';

PrimeReact.ripple = true;

startKea();

function Init() {
  useEffect(() => {
    startGlobalLogics();
  }, []);

  return (
    <InversifyProvider container={Dependencies}>
      <HistoryRouter>
        <App />
      </HistoryRouter>
    </InversifyProvider>
  );
}

createRoot(document.getElementById('app') as HTMLElement).render(<Init />);

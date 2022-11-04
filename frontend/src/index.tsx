import { Provider as InversifyProvider } from 'inversify-react';
import PrimeReact from 'primereact/api';
import { createRoot } from 'react-dom/client';

import { startGlobalLogics, startKea } from '@/logic';
import Pages from '@/pages';
import { history } from '@/pages/router';
import { SuspenseRouter } from '@/pages/router';
import '@/scss/global.scss';
import '@/scss/main.scss';

import Dependencies from './deps';
import './i18n';
import './logic';

PrimeReact.ripple = true;

startKea();
startGlobalLogics();

function Init() {
  return (
    <InversifyProvider container={Dependencies}>
      <SuspenseRouter history={history}>
        <Pages />
      </SuspenseRouter>
    </InversifyProvider>
  );
}

createRoot(document.getElementById('root') as HTMLElement).render(<Init />);
  
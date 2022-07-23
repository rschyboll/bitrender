import { Provider as InversifyProvider } from 'inversify-react';
import PrimeReact from 'primereact/api';
import { createRoot } from 'react-dom/client';

import { startKea } from '@/logic';
import Pages from '@/pages';
import { history } from '@/pages/history';
import { SuspenseRouter } from '@/pages/router';
import '@/scss/global.scss';
import '@/scss/main.scss';

import Dependencies from './deps';
import './i18n';
import './logic';

PrimeReact.ripple = true;

startKea();

function Init() {
  return (
    <InversifyProvider container={Dependencies}>
      <SuspenseRouter history={history}>
        <Pages />
      </SuspenseRouter>
    </InversifyProvider>
  );
}

createRoot(document.getElementById('app') as HTMLElement).render(<Init />);

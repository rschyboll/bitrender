import { Provider as InversifyProvider } from 'inversify-react';
import 'map.prototype.tojson';
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
import { AppLocalizationProvider } from './translations';
import { disableReactDevTools } from './utils/react';

PrimeReact.ripple = true;

startKea();
startGlobalLogics();

if (process.env.NODE_ENV == 'development') {
} else {
  disableReactDevTools();
}

function Init() {
  return (
    <InversifyProvider container={Dependencies}>
      <AppLocalizationProvider>
        <SuspenseRouter history={history}>
          <Pages />
        </SuspenseRouter>
      </AppLocalizationProvider>
    </InversifyProvider>
  );
}

createRoot(document.getElementById('root') as HTMLElement).render(<Init />);

import { LocalizationProvider, ReactLocalization } from '@fluent/react';
import { Children, ReactNode, useEffect, useState } from 'react';

import { Bundles } from './ftl';

interface AppLocalizationProviderProps {
  children: ReactNode;
}

export function AppLocalizationProvider(props: AppLocalizationProviderProps) {
  const [l10n, setL10n] = useState<ReactLocalization | null>(null);

  useEffect(() => {
    changeLocales(navigator.languages as Array<string>);
  }, []);

  async function changeLocales(userLocales: Array<string>) {
    setL10n(new ReactLocalization(Object.values(Bundles)));
  }

  if (l10n === null) {
    return <>LOADING</>;
  }

  return (
    <>
      <LocalizationProvider l10n={l10n}>
        {Children.only(props.children)}
      </LocalizationProvider>
    </>
  );
}

import { FluentBundle, FluentResource } from '@fluent/bundle';
import { negotiateLanguages } from '@fluent/langneg';
import { LocalizationProvider, ReactLocalization } from '@fluent/react';
import { Children, ReactNode, useEffect, useState } from 'react';

import Ftl from './ftl';

const DEFAULT_LOCALE = 'en';
const AVAILABLE_LOCALES = {
  en: 'English',
  pl: 'Polish',
};

async function fetchMessages(locale: string): Promise<[string, string]> {
  const response = await fetch(String(Ftl[locale]));
  const messages = await response.text();
  return [locale, messages];
}

function* lazilyParsedBundles(fetchedMessages: Array<[string, string]>) {
  for (const [locale, messages] of fetchedMessages) {
    const resource = new FluentResource(messages);
    const bundle = new FluentBundle(locale);
    bundle.addResource(resource);
    yield bundle;
  }
}

interface AppLocalizationProviderProps {
  children: ReactNode;
}

export function AppLocalizationProvider(props: AppLocalizationProviderProps) {
  const [l10n, setL10n] = useState<ReactLocalization | null>(null);

  useEffect(() => {
    changeLocales(navigator.languages as Array<string>);
  }, []);

  async function changeLocales(userLocales: Array<string>) {
    const currentLocales = negotiateLanguages(
      userLocales,
      Object.keys(AVAILABLE_LOCALES),
      { defaultLocale: DEFAULT_LOCALE },
    );

    const fetchedMessages = await Promise.all(
      currentLocales.map(fetchMessages),
    );

    const bundles = lazilyParsedBundles(fetchedMessages);
    setL10n(new ReactLocalization(bundles));
  }

  if (l10n === null) {
    return <>{props.children}</>;
  }

  return (
    <>
      <LocalizationProvider l10n={l10n}>
        {Children.only(props.children)}
      </LocalizationProvider>
    </>
  );
}

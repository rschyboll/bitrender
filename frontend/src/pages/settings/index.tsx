import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { RadioButton } from 'primereact/radiobutton';
import { Slider, SliderChangeParams } from 'primereact/slider';
import { memo, useCallback } from 'react';
import { Trans } from 'react-i18next';

import { Card, IconCard } from '@/components/card';
import { ISettingsLogic } from '@/logic/interfaces';
import { Theme } from '@/types/settings';

import './style.scss';

const SettingsPage = memo(function SettingsPage() {
  return (
    <div className="settings-page grid">
      <Card className="col-12 desktop:col-6" title="Rozkład aplikacji">
        Test
      </Card>
      <Card className="col-12 desktop:col-6" title="Motyw aplikacji">
        <ThemeSelector />
      </Card>
      <Card className="col-12 desktop:col-6" title="Rozmiar interfejsu">
        <FontSizeSelector />
      </Card>
    </div>
  );
});

const ThemeSelector = memo(function ThemeSelector() {
  return (
    <div className="theme-selector">
      <ThemeSelectorItem
        label="settings.theme.light"
        url={new URL('../../assets/theme-light.png', import.meta.url)}
        theme={Theme.Light}
      />
      <ThemeSelectorItem
        label="settings.theme.dim"
        url={new URL('../../assets/theme-dim.png', import.meta.url)}
        theme={Theme.Dim}
      />
      <ThemeSelectorItem
        label="settings.theme.dark"
        url={new URL('../../assets/theme-dark.png', import.meta.url)}
        theme={Theme.Dark}
      />
    </div>
  );
});

interface ThemePreviewProps {
  label: string;
  url: URL;
  theme: Theme;
}

const ThemeSelectorItem = memo(function ThemeSelectorItem(
  props: ThemePreviewProps,
) {
  const settingsLogic = useInjection(ISettingsLogic.$);

  const { theme } = useValues(settingsLogic);
  const { setTheme } = useActions(settingsLogic);

  const onClick = useCallback(() => {
    setTheme(props.theme);
  }, [props.theme, setTheme]);

  return (
    <div
      className={`theme-selector-item ${
        theme == props.theme ? 'selected' : ''
      }`}
      onClick={onClick}
    >
      <img className="theme-selector-image" src={props.url.pathname} />
      <span className="theme-selector-label">
        <Trans>{props.label}</Trans>
      </span>
    </div>
  );
});

const FontSizeSelector = memo(function FontSizeSelector() {
  const settingsLogic = useInjection(ISettingsLogic.$);

  const { fontSize } = useValues(settingsLogic);
  const { setFontSize } = useActions(settingsLogic);

  const onChange = useCallback(
    (e: SliderChangeParams) => {
      if (typeof e.value == 'number') {
        setFontSize(e.value);
      }
    },
    [setFontSize],
  );

  return (
    <div className="font-size-selector">
      <div className="font-size-slider">
        <span>-50%</span>
        <Slider min={10} max={18} value={fontSize} onChange={onChange} />
        <span>+50%</span>
      </div>
    </div>
  );
});

export default SettingsPage;

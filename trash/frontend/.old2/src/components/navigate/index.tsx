import { useInjection } from 'inversify-react';
import { useActions } from 'kea';
import { memo, useCallback, useEffect } from 'react';
import { Path } from 'react-router-dom';

import { IRouteLogic } from '@/logic/interfaces';

export interface NavigateProps {
  to: string | Partial<Path>;
  replace?: boolean;
  state?: object;
}

export const Navigate = memo(function Navigate(props: NavigateProps) {
  const { to, replace, state } = props;

  const routeLogic = useInjection(IRouteLogic.$);

  const { openRoute, replaceRoute } = useActions(routeLogic);

  const onLinkClick = useCallback(() => {
    if (replace == true) {
      replaceRoute(to, state);
    } else {
      openRoute(to, state);
    }
  }, [openRoute, replace, replaceRoute, state, to]);

  useEffect(() => {
    onLinkClick();
  }, [onLinkClick]);

  return null;
});

import { useInjection } from 'inversify-react';
import { useActions } from 'kea';
import React, { memo, useCallback } from 'react';
import { Path } from 'react-router-dom';

import { IRouteLogic } from '@/logic/interfaces';

import './style.scss';

export interface LinkProps extends React.HTMLAttributes<HTMLAnchorElement> {
  to: string | Partial<Path>;
  replace?: boolean;
  state?: object;
}

export const Link = memo(function Link(props: LinkProps) {
  const { to, replace, state, onClick, children, ...anchorProps } = props;

  const routeLogic = useInjection(IRouteLogic.$);

  const { openRoute, replaceRoute } = useActions(routeLogic);

  const onLinkClick = useCallback(
    (e: React.MouseEvent<HTMLAnchorElement>) => {
      if (onClick != null) {
        onClick(e);
      }
      if (replace == true) {
        replaceRoute(to, state);
      } else {
        openRoute(to, state);
      }
    },
    [onClick, openRoute, replace, replaceRoute, state, to],
  );

  return (
    <a className="link" onClick={onLinkClick} {...anchorProps}>
      {children}
    </a>
  );
});

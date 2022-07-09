import { createBrowserHistory } from 'history';
import { FC, useLayoutEffect, useState } from 'react';
import { HistoryRouterProps, Router } from 'react-router-dom';

export const history = createBrowserHistory();

export const HistoryRouter: FC<HistoryRouterProps> = ({
  history,
  ...props
}) => {
  const [state, setState] = useState({
    action: history.action,
    location: history.location,
  });

  useLayoutEffect(() => history.listen(setState), [history]);

  return (
    <Router
      {...props}
      location={state.location}
      navigationType={state.action}
      navigator={history}
    />
  );
};

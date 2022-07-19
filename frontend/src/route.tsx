import { createBrowserHistory } from 'history';
import { FC } from 'react';
import { unstable_HistoryRouter as ReactHistoryRouter } from 'react-router-dom';

export const history = createBrowserHistory({ window: window });


export const HistoryRouter: FC<{ children: JSX.Element[] | JSX.Element }> = (
  props,
) => {
  return (
    <ReactHistoryRouter history={history}>{props.children}</ReactHistoryRouter>
  );
};

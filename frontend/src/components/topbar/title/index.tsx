import { memo } from 'react';
import { Trans } from 'react-i18next';
import { useLocation } from 'react-router-dom';

import './style.scss';

const pathNameTitles: Record<string, string | undefined> = {
  '/app/admin/roles': 'nav.roles',
  '/app/admin/users': 'nav.users',
};

export const TopbarTitle = memo(function TopbarTitle() {
  const location = useLocation();

  let title = pathNameTitles[location.pathname];

  if (title == null) {
    title = '';
  }

  return (
    <span className="topbar-title">
      <Trans>{title}</Trans>
    </span>
  );
});

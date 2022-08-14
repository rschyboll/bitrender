import { useInjection } from 'inversify-react';
import { useActions } from 'kea';
import { Card } from 'primereact/card';
import { memo } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { IRouteLogic } from '@/logic/interfaces';

import './style.scss';

const EntryPage = memo(function EntryPage() {
  const routeLogic = useInjection(IRouteLogic.$);

  const { openApp, openRolesPage, openUsersPage } = useActions(routeLogic);
  const navigate = useNavigate();

  return (
    <Card id="entry-page-card" className="shadow-2">
      <Logo titleVisible={true} />
      <div id="entry-page-card-content">
        <Outlet />
      </div>
      <button onClick={openApp}>App</button>
      <button onClick={() => navigate('/app/admin/roles')}>Roles</button>
      <button onClick={openUsersPage}>Users</button>
    </Card>
  );
});

export default EntryPage;

import { Card } from 'primereact/card';
import { memo } from 'react';
import { Outlet } from 'react-router-dom';

import { Logo } from '@/components/logo';

import './style.scss';

const EntryPage = memo(function EntryPage() {
  return (
    <Card id="entry-page-card" className="shadow-2">
      <Logo titleVisible={true} />
      <div id="entry-page-card-content">
        <Outlet />
      </div>
    </Card>
  );
});

export default EntryPage;

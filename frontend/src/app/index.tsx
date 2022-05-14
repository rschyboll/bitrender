import { FC, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Outlet, Route, Routes } from 'react-router-dom';

import { Sidebar } from '@/components/sidebar';
import { RolesPage } from '@/pages/roles';
import { UsersPage } from '@/pages/users';

import './style.scss';

export const App: FC = () => {
  useEffect(() => {
    const themeLink = document.getElementById('theme-link');
    if (themeLink instanceof HTMLLinkElement) {
      themeLink.href = 'themes/arya-orange.css';
    }
  }, []);

  return (
    <Routes>
      <Route path="/" element={<AppBody />}>
        <Route path="users" element={<UsersPage />} />
        <Route path="roles" element={<RolesPage />} />
      </Route>
    </Routes>
  );
};

export const AppBody: FC = () => {
  return (
    <div className="layout h-full">
      <div className="layout-sidebar">
        <Sidebar />
      </div>
      <div className="layout-content">
        <div className="layout-topbar"></div>
        <div className="layout-page">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

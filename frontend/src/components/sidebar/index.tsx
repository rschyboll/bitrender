import { useValues } from 'kea';
import { FC, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Trans } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';

import { settingsLogic } from '@/logic/settings';

import { sidebarModel } from './model';
import './style.scss';

const logo = new URL('../../assets/logo.svg', import.meta.url);

export const Sidebar: FC = () => {
  const location = useLocation();
  const { sidebarType } = useValues(settingsLogic);

  return (
    <div className="sidebar">
      <Link className="logo" to="/">
        <img
          id="app-logo"
          className="logo-image"
          src={logo.toString()}
          alt="diamond layout"
        />
        <span className="app-name">BITRENDER </span>
      </Link>
      <ul className="sidebar-container">
        {Object.entries(sidebarModel).map((entry) => {
          return (
            <li className="sidebar-group" key={entry[0]}>
              <div className="sidebar-group-title">
                <Trans>FAVORITES</Trans>
              </div>
              {entry[1].items.map((item) => {
                return <div key={item.path}> </div>;
              })}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

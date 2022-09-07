import { Card as PrimeCard } from 'primereact/card';
import { ReactNode, memo } from 'react';
import { Trans } from 'react-i18next';
import { IconType } from 'react-icons';

import './style.scss';

export interface CardProps {
  id?: string;
  className?: string;
  title?: string;
  titleActions?: ReactNode;
  children: ReactNode;
}

export const Card = memo(function IconCard(props: CardProps) {
  return (
    <div className={`card ${props.className}`}>
      <PrimeCard>{props.children}</PrimeCard>
    </div>
  );
});

export interface IconCardProps {
  id?: string;
  className?: string;
  title: string;
  color: string;
  icon: IconType;
  iconSize?: string;
  children: ReactNode;
}

export const IconCard = memo(function IconCard(props: IconCardProps) {
  return (
    <div className={`icon-card ${props.className}`}>
      <PrimeCard style={{ borderColor: props.color }}>
        <div className="icon-card-header">
          <div
            className="icon-card-icon-box"
            style={{ backgroundColor: props.color }}
          >
            <props.icon
              className="icon-card-icon"
              color={'rgba(0, 0, 0, 0.75)'}
            />
          </div>
          <span className="icon-card-title" style={{ color: props.color }}>
            <Trans>{props.title}</Trans>
          </span>
        </div>
      </PrimeCard>
    </div>
  );
});

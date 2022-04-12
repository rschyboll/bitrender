import { FunctionComponent } from 'react';
import { Link } from 'react-router-dom';

export const App: FunctionComponent = () => {
  return (
    <div>
      <h1>Bookkeeper</h1>
      <Link to="/invoices">Invoices</Link> |{' '}
      <Link to="/expenses">Expenses</Link>
    </div>
  );
};

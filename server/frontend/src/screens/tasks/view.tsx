import { FunctionComponent } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { PrimeIcons } from "primereact/api";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { DataTable } from "primereact/datatable";

const TableHeader: FunctionComponent = () => {
  const { t } = useTranslation();

  return (
    <div>
      <Link className="link" to="/addTask">
        <Button icon={PrimeIcons.PLUS} label={t("tasks.new")} />
      </Link>
    </div>
  );
};

export type TasksViewProps = {};

export const TasksView: FunctionComponent<TasksViewProps> = () => {
  return (
    <Card>
      <DataTable header={<TableHeader />} />
    </Card>
  );
};

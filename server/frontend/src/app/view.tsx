import { FunctionComponent } from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import { Sidebar } from "components/sidebar";
import { Topbar } from "components/topbar";
import { Tasks } from "screens/tasks";
import { AddTask } from "screens/addTask";

export const AppView: FunctionComponent = () => {
  return (
    <div id="layout-base">
      <BrowserRouter>
        <div id="layout-sidebar">
          <Sidebar />
        </div>
        <div id="layout-content-wrapper">
          <div id="layout-topbar">
            <Topbar />
          </div>
          <div id="layout-content">
            <Switch>
              <Route path="/machines">Hello3</Route>
              <Route path="/tasks">
                <Tasks />
              </Route>

              <Route path="/addTask">
                <AddTask />
              </Route>
              <Route path="/">Hello</Route>
            </Switch>
          </div>
        </div>
      </BrowserRouter>
    </div>
  );
};

// Page layout. Owner: Person 3.
// Each component is owned by someone else: see the comment at the top of each file.

import { useState } from "react";

import PersonaSwitcher from "./components/PersonaSwitcher.jsx";
import UploadStatement from "./components/UploadStatement.jsx";
import CategorisedBadge from "./components/CategorisedBadge.jsx";
import HeadlineCard from "./components/HeadlineCard.jsx";
import BreakdownChart from "./components/BreakdownChart.jsx";
import HistoryChart from "./components/HistoryChart.jsx";
import InflationProofToggle from "./components/InflationProofToggle.jsx";
import SpacesPanel from "./components/SpacesPanel.jsx";
import SourceFooter from "./components/SourceFooter.jsx";

export default function App() {
  const [accountId, setAccountId] = useState("1"); // the student renter in the seed data

  return (
    <div className="app">
      <header className="app-header">
        <h1>Meflation</h1>
        <PersonaSwitcher accountId={accountId} onChange={setAccountId} />
      </header>

      <main className="grid">
        <div className="span-2">
          <HeadlineCard accountId={accountId} />
        </div>
        <BreakdownChart accountId={accountId} />
        <HistoryChart accountId={accountId} />
        <InflationProofToggle accountId={accountId} />
        <SpacesPanel accountId={accountId} />
        <CategorisedBadge accountId={accountId} />
        <UploadStatement onImported={setAccountId} />
      </main>

      <SourceFooter />
    </div>
  );
}

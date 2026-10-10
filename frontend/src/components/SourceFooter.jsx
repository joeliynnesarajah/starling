// Owner: Person 3
// "Source: ONS CPIH, fetched [date]". Small, but it makes the numbers believable.
// Data: getInflationHistory().source

import { useEffect, useState } from "react";
import { getInflationHistory } from "../api.js";

export default function SourceFooter() {
  const [source, setSource] = useState(null);

  useEffect(() => {
    let cancelled = false;
    getInflationHistory(1)
      .then((data) => !cancelled && setSource(data.source))
      .catch(() => {}); // the footer is not worth an error message
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <footer className="footer">
      Source: {source ?? "ONS CPIH"}
    </footer>
  );
}

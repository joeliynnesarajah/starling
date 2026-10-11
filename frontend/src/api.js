// Every call to the backend goes through this file.
// Shared file: Person 3 sets it up, each person fills in their own functions.
//
// While VITE_USE_MOCK=true, functions return the fake JSON in src/mock/,
// so nobody is blocked waiting for the backend. Switch to false by Day 1 evening.

import mockAccounts from "./mock/accounts.json";
import mockPersonalRate from "./mock/personal-rate.json";
import mockPersonalHistory from "./mock/personal-history.json";
import mockInflationHistory from "./mock/inflation-history.json";
import mockSpaces from "./mock/spaces.json";
import mockSummary from "./mock/categorised-summary.json";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const USE_MOCK = (import.meta.env.VITE_USE_MOCK ?? "true") !== "false";

const fake = (data) => new Promise((resolve) => setTimeout(() => resolve(data), 200));

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);
  if (!response.ok) {
    throw new Error(`${options.method ?? "GET"} ${path} failed: ${response.status}`);
  }
  return response.status === 204 ? null : response.json();
}

const post = (path, body) =>
  request(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

// --- Person 1 -------------------------------------------------------------

export const getAccounts = () => (USE_MOCK ? fake(mockAccounts) : request("/accounts"));

// Fake mode keeps its own copy of the Spaces so "Simulate next month" visibly works.
// Same rules as the Engine, minus the balance check. Resets on page refresh.
const mockBank = { today: "2026-01-31", ...structuredClone(mockSpaces) };

// "2026-01-31" -> "2026-02-28": same day next month, clamped like the Engine's add_month
function addMonth(iso) {
  const [y, m, d] = iso.split("-").map(Number);
  const [year, month] = m === 12 ? [y + 1, 1] : [y, m + 1];
  const lastDay = new Date(year, month, 0).getDate();
  return `${year}-${String(month).padStart(2, "0")}-${String(Math.min(d, lastDay)).padStart(2, "0")}`;
}

function fakeNextMonth() {
  mockBank.today = addMonth(mockBank.today);
  const ran = [];
  for (const order of mockBank.standing_orders) {
    if (order.next_run_date > mockBank.today) continue;
    mockBank.spaces.find((s) => s.id === order.space_id).balance_pence += order.amount_pence;
    ran.push({ standing_order_id: order.id, space_id: order.space_id, amount_pence: order.amount_pence });
    while (order.next_run_date <= mockBank.today) order.next_run_date = addMonth(order.next_run_date);
  }
  return { today: mockBank.today, ran };
}

export const getSpaces = (accountId) =>
  USE_MOCK
    ? fake(
        structuredClone({
          spaces: mockBank.spaces.filter((s) => s.account_id === String(accountId)),
          standing_orders: mockBank.standing_orders.filter((o) => o.account_id === String(accountId)),
        }),
      )
    : request(`/accounts/${accountId}/spaces`);

export const simulateNextMonth = () =>
  USE_MOCK ? fake(fakeNextMonth()) : post("/simulate/next-month", {});

// --- Person 2 -------------------------------------------------------------

export const getCategorisedSummary = (accountId) =>
  USE_MOCK ? fake(mockSummary) : request(`/categorised/summary?account_id=${accountId}`);

export async function uploadStatement(file, accountName) {
  // Fake mode: pretend the upload worked, so we can build without the backend
  if (USE_MOCK) {
    return fake({ account_id: 5, inserted: 42, summary: mockSummary });
  }
  const form = new FormData();
  form.append("file", file);
  return request(`/statements/upload?account_name=${encodeURIComponent(accountName)}`, {
    method: "POST",
    body: form,
  });
}

// --- Person 3 -------------------------------------------------------------

export const getInflationHistory = (months = 12) =>
  USE_MOCK ? fake(mockInflationHistory) : request(`/inflation/history?months=${months}`);

// --- Person 4 -------------------------------------------------------------

export const getPersonalRate = (accountId) =>
  USE_MOCK ? fake(mockPersonalRate) : request(`/personal-rate?account_id=${accountId}`);

export const getPersonalHistory = (accountId) =>
  USE_MOCK ? fake(mockPersonalHistory) : request(`/personal-rate/history?account_id=${accountId}`);

export const setInflationProof = (accountId, enabled) =>
  USE_MOCK
    ? fake({ account_id: accountId, enabled, monthly_top_up_pence: enabled ? 850 : 0 })
    : post("/inflation-proof", { account_id: accountId, enabled });

export const getInflationProof = (accountId) =>
  USE_MOCK
    ? fake({ account_id: accountId, enabled: false, monthly_top_up_pence: 0 })
    : request(`/inflation-proof?account_id=${accountId}`);

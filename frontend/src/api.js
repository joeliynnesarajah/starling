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

export const getSpaces = (accountId) =>
  USE_MOCK ? fake(mockSpaces) : request(`/accounts/${accountId}/spaces`);

export const simulateNextMonth = () =>
  USE_MOCK ? fake({ today: "2026-11-01", ran: [] }) : post("/simulate/next-month", {});

// --- Person 2 -------------------------------------------------------------

export const getCategorisedSummary = (accountId) =>
  USE_MOCK ? fake(mockSummary) : request(`/categorised/summary?account_id=${accountId}`);

export async function uploadStatement(file, accountName) {
  // TODO(Person 2): mock branch can return a fake StatementImportResponse
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

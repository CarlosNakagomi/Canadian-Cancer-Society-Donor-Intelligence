const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const RAW_TXT = path.join(ROOT, "data/raw/GVP_DBP_2023/Data_Données/GVP_DBP_2023_PUMF_FMGD.txt");
const OUT_DOC = path.join(ROOT, "outputs/data_understanding");
const OUT_CH1 = path.join(ROOT, "outputs/chapter1");
const OUT_DATA = path.join(ROOT, "data/processed");

for (const dir of [OUT_DOC, OUT_CH1, OUT_DATA]) fs.mkdirSync(dir, { recursive: true });

const vars = [
  {
    name: "WGHT_PER",
    start: 6,
    end: 15,
    type: "decimal",
    label: "Person weight",
    values: [],
    special: {
      "99999.9996": "Valid skip",
      "99999.9997": "Don't know",
      "99999.9998": "Refusal",
      "99999.9999": "Not stated",
    },
    universe: "All respondents; survey person weight for population-level estimates.",
    role: "Survey weight",
    treatment: "Keep as numeric survey weight. Do not impute. Exclude only if a documented special code appears.",
  },
  {
    name: "AGEGR10",
    start: 16,
    end: 17,
    type: "integer",
    label: "Age group of respondent (groups of 10)",
    values: {
      "1": "15 to 24 years",
      "2": "25 to 34 years",
      "3": "35 to 44 years",
      "4": "45 to 54 years",
      "5": "55 to 64 years",
      "6": "65 to 74 years",
      "7": "75 years and over",
    },
    special: { "96": "Valid skip", "97": "Don't know", "98": "Refusal", "99": "Not stated" },
    universe: "All respondents.",
    role: "Demographic segment",
    treatment: "Keep labelled valid groups. Treat only documented special codes as non-analytic.",
  },
  {
    name: "GENDER2",
    start: 18,
    end: 18,
    type: "integer",
    label: "Gender of respondent after distribution of non-binary persons",
    values: { "1": "Man+", "2": "Woman+" },
    special: { "6": "Valid skip", "7": "Don't know", "8": "Refusal", "9": "Not stated" },
    universe: "All respondents.",
    role: "Demographic segment",
    treatment: "Keep labelled valid groups. Treat only documented special codes as non-analytic.",
  },
  {
    name: "PRV",
    start: 34,
    end: 35,
    type: "integer",
    label: "Province of residence",
    values: {
      "10": "Newfoundland and Labrador",
      "11": "Prince Edward Island",
      "12": "Nova Scotia",
      "13": "New Brunswick",
      "24": "Quebec",
      "35": "Ontario",
      "46": "Manitoba",
      "47": "Saskatchewan",
      "48": "Alberta",
      "59": "British Columbia",
    },
    special: { "96": "Valid skip", "97": "Don't know", "98": "Refusal", "99": "Not stated" },
    universe: "All respondents.",
    role: "Geographic segment",
    treatment: "Keep labelled valid provinces. Treat documented special codes as non-analytic.",
  },
  {
    name: "FG1FGIV",
    start: 875,
    end: 875,
    type: "integer",
    label: "Giving flag",
    values: { "1": "Giver", "2": "Non-giver" },
    special: { "6": "Valid skip", "7": "Don't know", "8": "Refusal", "9": "Not stated" },
    universe: "All respondents.",
    role: "Primary donor participation outcome",
    treatment: "Map 1 to donor and 2 to non-donor. Treat documented special codes as non-analytic if present.",
    note: "A giver is defined as a respondent with at least one 'yes' in FG1A_030 to FG1A_170.",
  },
  {
    name: "GS1DNTOT",
    start: 1059,
    end: 1060,
    type: "integer",
    label: "Total number of financial donations",
    values: "Numeric count of financial donations; observed donor counts in this file run from 1 to 26.",
    special: { "96": "Valid skip", "97": "Don't know", "98": "Refusal", "99": "Not stated" },
    universe: "FG1FGIV = 1.",
    role: "Donation frequency outcome among donors",
    treatment: "For donors, keep valid numeric counts. For non-givers, retain raw 96 as valid skip and set analytical count to null.",
    note: "Derived count of financial donations made to organizations, including up to a maximum of 7 donations for each solicitation method.",
  },
  {
    name: "GS1DATOT",
    start: 1061,
    end: 1072,
    type: "decimal",
    label: "Total amount of donations",
    values: "Amount in dollars; codebook donor amount range: 000000000.50 to 000138800.00. Code 000000000.00 means None.",
    special: {
      "000000000.00": "None",
      "999999999.96": "Valid skip",
      "999999999.97": "Don't know",
      "999999999.98": "Refusal",
      "999999999.99": "Not stated",
    },
    universe: "FG1FGIV = 1.",
    role: "Donation amount outcome among donors",
    treatment: "For donors, keep valid dollar amounts. For non-givers, retain raw 999999999.96 as valid skip and set analytical amount to null.",
    note: "All 'other' donations (GSA_080) are included in the total amount.",
  },
  {
    name: "ED4CAT",
    start: 1528,
    end: 1528,
    type: "integer",
    label: "Education - Highest degree (4 categories)",
    values: {
      "1": "Less than high school",
      "2": "Graduated from high school",
      "3": "Post-secondary diploma",
      "4": "University diploma",
    },
    special: { "6": "Valid skip", "7": "Don't know", "8": "Refusal", "9": "Not stated" },
    universe: "All respondents.",
    role: "Socioeconomic segment",
    treatment: "Keep labelled valid groups. Treat documented special codes as non-analytic.",
  },
  {
    name: "INCG2",
    start: 1612,
    end: 1613,
    type: "integer",
    label: "Income - Personal income group (before tax)",
    values: {
      "1": "Less than $25,000",
      "2": "$25,000 to $49,999",
      "3": "$50,000 to $74,999",
      "4": "$75,000 to $99,999",
      "5": "$100,000 to $124,999",
      "6": "$125,000 and more",
    },
    special: { "96": "Valid skip", "97": "Don't know", "98": "Refusal", "99": "Not stated" },
    universe: "All respondents.",
    role: "Socioeconomic segment",
    treatment: "Keep labelled valid groups. Treat documented special codes as non-analytic.",
  },
  {
    name: "FAMINCG2",
    start: 1615,
    end: 1616,
    type: "integer",
    label: "Family income - Family income group (before tax)",
    values: {
      "1": "Less than $25,000",
      "2": "$25,000 to $49,999",
      "3": "$50,000 to $74,999",
      "4": "$75,000 to $99,999",
      "5": "$100,000 to $124,999",
      "6": "$125,000 and more",
    },
    special: { "96": "Valid skip", "97": "Don't know", "98": "Refusal", "99": "Not stated" },
    universe: "All respondents.",
    role: "Socioeconomic segment",
    treatment: "Keep labelled valid groups. Treat documented special codes as non-analytic.",
  },
];

function rawField(line, spec) {
  return line.slice(spec.start - 1, spec.end).trim();
}

function parseField(line, spec) {
  const raw = rawField(line, spec);
  if (raw === "") return { raw, value: null, label: "Blank" };
  const num = Number(raw);
  const key = String(num);
  const fixed2 = Number.isFinite(num) ? num.toFixed(2).padStart(12, "0") : raw;
  const fixed4 = Number.isFinite(num) ? num.toFixed(4).padStart(10, "0") : raw;
  const specialLabel = spec.special[raw] || spec.special[key] || spec.special[fixed2] || spec.special[fixed4];
  if (specialLabel) return { raw, value: num, label: specialLabel };
  if (typeof spec.values === "object" && !Array.isArray(spec.values)) {
    return { raw, value: num, label: spec.values[key] || spec.values[raw] || "Unlabelled code" };
  }
  return { raw, value: num, label: "Valid numeric" };
}

function csvEscape(v) {
  if (v === null || v === undefined) return "";
  const s = String(v);
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function writeCsv(file, rows, headers) {
  const data = [headers.join(",")]
    .concat(rows.map((r) => headers.map((h) => csvEscape(r[h])).join(",")))
    .join("\n");
  fs.writeFileSync(file, data + "\n", "utf8");
}

function weightedMean(rows, valueKey, weightKey = "WGHT_PER") {
  let sw = 0;
  let sx = 0;
  for (const r of rows) {
    const x = r[valueKey];
    const w = r[weightKey];
    if (Number.isFinite(x) && Number.isFinite(w)) {
      sw += w;
      sx += x * w;
    }
  }
  return sw ? sx / sw : null;
}

function weightedMedian(rows, valueKey, weightKey = "WGHT_PER") {
  const valid = rows
    .filter((r) => Number.isFinite(r[valueKey]) && Number.isFinite(r[weightKey]))
    .sort((a, b) => a[valueKey] - b[valueKey]);
  const total = valid.reduce((s, r) => s + r[weightKey], 0);
  const half = total / 2;
  let run = 0;
  for (const r of valid) {
    run += r[weightKey];
    if (run >= half) return r[valueKey];
  }
  return null;
}

function pct(n, d) {
  return d ? (100 * n) / d : null;
}

const text = fs.readFileSync(RAW_TXT, "utf8");
const lines = text.split(/\r?\n/).filter((line) => line.length > 0);
const rawHash = require("crypto").createHash("sha256").update(fs.readFileSync(RAW_TXT)).digest("hex");

const rows = lines.map((line) => {
  const r = {};
  for (const spec of vars) {
    const parsed = parseField(line, spec);
    r[spec.name] = parsed.value;
    r[`${spec.name}_raw`] = parsed.raw;
    r[`${spec.name}_label`] = parsed.label;
  }
  r.is_donor = r.FG1FGIV === 1;
  r.donation_amount = r.FG1FGIV === 1 && r.GS1DATOT < 999999999 ? r.GS1DATOT : null;
  r.donation_count = r.FG1FGIV === 1 && r.GS1DNTOT < 96 ? r.GS1DNTOT : null;
  return r;
});

const dictRows = [];
for (const v of vars) {
  const validValues = typeof v.values === "string" ? v.values : Object.entries(v.values).map(([k, val]) => `${k}=${val}`).join("; ");
  const special = Object.entries(v.special).map(([k, val]) => `${k}=${val}`).join("; ");
  dictRows.push({
    variable_name: v.name,
    official_label: v.label,
    position: `${v.start}-${v.end}`,
    valid_values_categories: validValues,
    special_codes: special,
    valid_skip: Object.entries(v.special).filter(([, val]) => val === "Valid skip").map(([k]) => k).join("; "),
    dont_know: Object.entries(v.special).filter(([, val]) => val === "Don't know").map(([k]) => k).join("; "),
    refusal: Object.entries(v.special).filter(([, val]) => val === "Refusal").map(([k]) => k).join("; "),
    not_stated: Object.entries(v.special).filter(([, val]) => val === "Not stated").map(([k]) => k).join("; "),
    universe_applicability: v.universe,
    analytical_role: v.role,
    proposed_treatment: v.treatment,
    official_note: v.note || "",
    source: "SGVP 2023 PUMF English data dictionary/codebook and English SAS/STATA layout files",
  });
}
writeCsv(path.join(OUT_DOC, "variable_dictionary.csv"), dictRows, Object.keys(dictRows[0]));

const dqaRows = [];
for (const v of vars) {
  const counts = new Map();
  let validN = 0;
  let specialN = 0;
  for (const r of rows) {
    const raw = r[`${v.name}_raw`];
    const label = r[`${v.name}_label`];
    const key = `${raw}||${label}`;
    counts.set(key, (counts.get(key) || 0) + 1);
    if (Object.values(v.special).includes(label)) specialN += 1;
    else validN += 1;
  }
  for (const [key, count] of Array.from(counts.entries()).sort((a, b) => b[1] - a[1])) {
    const [raw, label] = key.split("||");
    dqaRows.push({
      variable_name: v.name,
      raw_value: raw,
      value_label: label,
      sample_n: count,
      sample_pct: pct(count, rows.length).toFixed(2),
      weighted_population_estimate: rows
        .filter((r) => r[`${v.name}_raw`] === raw)
        .reduce((s, r) => s + r.WGHT_PER, 0)
        .toFixed(0),
      issue_type: Object.values(v.special).includes(label) ? label : "Valid observed value",
    });
  }
  dqaRows.push({
    variable_name: v.name,
    raw_value: "__SUMMARY__",
    value_label: "Valid vs documented special-code profile",
    sample_n: rows.length,
    sample_pct: "100.00",
    weighted_population_estimate: rows.reduce((s, r) => s + r.WGHT_PER, 0).toFixed(0),
    issue_type: `${validN} valid-coded rows; ${specialN} special-coded rows`,
  });
}
writeCsv(path.join(OUT_DOC, "data_quality_profile.csv"), dqaRows, Object.keys(dqaRows[0]));

const analyticHeaders = [
  "WGHT_PER",
  "FG1FGIV",
  "donor_status",
  "donation_amount",
  "donation_count",
  "AGEGR10",
  "age_group",
  "GENDER2",
  "gender",
  "PRV",
  "province",
  "INCG2",
  "personal_income",
  "FAMINCG2",
  "family_income",
  "ED4CAT",
  "education",
];
const analyticRows = rows.map((r) => ({
  WGHT_PER: r.WGHT_PER,
  FG1FGIV: r.FG1FGIV,
  donor_status: r.FG1FGIV_label,
  donation_amount: r.donation_amount,
  donation_count: r.donation_count,
  AGEGR10: r.AGEGR10,
  age_group: r.AGEGR10_label,
  GENDER2: r.GENDER2,
  gender: r.GENDER2_label,
  PRV: r.PRV,
  province: r.PRV_label,
  INCG2: r.INCG2,
  personal_income: r.INCG2_label,
  FAMINCG2: r.FAMINCG2,
  family_income: r.FAMINCG2_label,
  ED4CAT: r.ED4CAT,
  education: r.ED4CAT_label,
}));
writeCsv(path.join(OUT_DATA, "sgvp_2023_chapter1_analytical.csv"), analyticRows, analyticHeaders);

function overallSummary() {
  const totalW = rows.reduce((s, r) => s + r.WGHT_PER, 0);
  const donors = rows.filter((r) => r.is_donor);
  const donorW = donors.reduce((s, r) => s + r.WGHT_PER, 0);
  return [{
    metric: "Respondents",
    sample_value: rows.length,
    weighted_value: totalW.toFixed(0),
    note: "Weighted value estimates Canadian population represented by respondents.",
  }, {
    metric: "Donors",
    sample_value: donors.length,
    weighted_value: donorW.toFixed(0),
    note: "FG1FGIV = 1.",
  }, {
    metric: "Donor participation rate",
    sample_value: pct(donors.length, rows.length).toFixed(1) + "%",
    weighted_value: pct(donorW, totalW).toFixed(1) + "%",
    note: "Use weighted rate for population-level reporting.",
  }, {
    metric: "Mean donation among donors",
    sample_value: (donors.reduce((s, r) => s + r.donation_amount, 0) / donors.length).toFixed(2),
    weighted_value: weightedMean(donors, "donation_amount").toFixed(2),
    note: "Donation amounts are among donors only.",
  }, {
    metric: "Median donation among donors",
    sample_value: donors.map((r) => r.donation_amount).sort((a, b) => a - b)[Math.floor(donors.length / 2)],
    weighted_value: weightedMedian(donors, "donation_amount").toFixed(2),
    note: "Median is preferred over mean for skewed donation amounts.",
  }, {
    metric: "Mean donation frequency among donors",
    sample_value: (donors.reduce((s, r) => s + r.donation_count, 0) / donors.length).toFixed(2),
    weighted_value: weightedMean(donors, "donation_count").toFixed(2),
    note: "Frequency is total number of financial donations.",
  }, {
    metric: "Median donation frequency among donors",
    sample_value: donors.map((r) => r.donation_count).sort((a, b) => a - b)[Math.floor(donors.length / 2)],
    weighted_value: weightedMedian(donors, "donation_count").toFixed(2),
    note: "Frequency is among donors only.",
  }];
}
writeCsv(path.join(OUT_CH1, "chapter1_overall_summary.csv"), overallSummary(), ["metric", "sample_value", "weighted_value", "note"]);

function segmentSummary(varName, labelName) {
  const groups = new Map();
  for (const r of rows) {
    const label = r[labelName];
    if (!label || ["Valid skip", "Don't know", "Refusal", "Not stated"].includes(label)) continue;
    if (!groups.has(label)) groups.set(label, []);
    groups.get(label).push(r);
  }
  return Array.from(groups.entries()).map(([segment, g]) => {
    const donors = g.filter((r) => r.is_donor);
    const totalW = g.reduce((s, r) => s + r.WGHT_PER, 0);
    const donorW = donors.reduce((s, r) => s + r.WGHT_PER, 0);
    return {
      segment_variable: varName,
      segment,
      sample_n: g.length,
      weighted_population: totalW.toFixed(0),
      sample_donor_rate_pct: pct(donors.length, g.length).toFixed(1),
      weighted_donor_rate_pct: pct(donorW, totalW).toFixed(1),
      donor_sample_n: donors.length,
      weighted_donors: donorW.toFixed(0),
      weighted_mean_donation: donors.length ? weightedMean(donors, "donation_amount").toFixed(2) : "",
      weighted_median_donation: donors.length ? weightedMedian(donors, "donation_amount").toFixed(2) : "",
      weighted_mean_frequency: donors.length ? weightedMean(donors, "donation_count").toFixed(2) : "",
      weighted_median_frequency: donors.length ? weightedMedian(donors, "donation_count").toFixed(2) : "",
    };
  });
}

const segmentRows = []
  .concat(segmentSummary("AGEGR10", "AGEGR10_label"))
  .concat(segmentSummary("GENDER2", "GENDER2_label"))
  .concat(segmentSummary("PRV", "PRV_label"))
  .concat(segmentSummary("INCG2", "INCG2_label"))
  .concat(segmentSummary("FAMINCG2", "FAMINCG2_label"))
  .concat(segmentSummary("ED4CAT", "ED4CAT_label"));
writeCsv(path.join(OUT_CH1, "chapter1_segment_summary_powerbi.csv"), segmentRows, Object.keys(segmentRows[0]));

const donors = rows.filter((r) => r.is_donor);
const amountBands = [
  { band: "$0.50 to $49", min: 0.5, max: 49.999 },
  { band: "$50 to $99", min: 50, max: 99.999 },
  { band: "$100 to $249", min: 100, max: 249.999 },
  { band: "$250 to $499", min: 250, max: 499.999 },
  { band: "$500 to $999", min: 500, max: 999.999 },
  { band: "$1,000 to $4,999", min: 1000, max: 4999.999 },
  { band: "$5,000 and over", min: 5000, max: Infinity },
];
const amountBandRows = amountBands.map((b) => {
  const g = donors.filter((r) => r.donation_amount >= b.min && r.donation_amount <= b.max);
  const weightedDonors = g.reduce((s, r) => s + r.WGHT_PER, 0);
  const weightedDollars = g.reduce((s, r) => s + r.WGHT_PER * r.donation_amount, 0);
  return {
    amount_band: b.band,
    donor_sample_n: g.length,
    weighted_donors: weightedDonors.toFixed(0),
    weighted_donor_share_pct: pct(weightedDonors, donors.reduce((s, r) => s + r.WGHT_PER, 0)).toFixed(1),
    weighted_total_donations: weightedDollars.toFixed(0),
    weighted_dollar_share_pct: pct(weightedDollars, donors.reduce((s, r) => s + r.WGHT_PER * r.donation_amount, 0)).toFixed(1),
  };
});
writeCsv(path.join(OUT_CH1, "chapter1_donation_amount_bands_powerbi.csv"), amountBandRows, Object.keys(amountBandRows[0]));

const freqCounts = new Map();
for (const r of donors) {
  const key = String(r.donation_count);
  if (!freqCounts.has(key)) freqCounts.set(key, []);
  freqCounts.get(key).push(r);
}
const frequencyRows = Array.from(freqCounts.entries())
  .sort((a, b) => Number(a[0]) - Number(b[0]))
  .map(([count, g]) => {
    const weightedDonors = g.reduce((s, r) => s + r.WGHT_PER, 0);
    return {
      donation_count: count,
      donor_sample_n: g.length,
      weighted_donors: weightedDonors.toFixed(0),
      weighted_donor_share_pct: pct(weightedDonors, donors.reduce((s, r) => s + r.WGHT_PER, 0)).toFixed(1),
    };
  });
writeCsv(path.join(OUT_CH1, "chapter1_donation_frequency_powerbi.csv"), frequencyRows, Object.keys(frequencyRows[0]));

const amountValues = donors.map((r) => r.donation_amount).sort((a, b) => a - b);
const topAmount = amountValues.slice(-20).reverse();
const validationRows = [
  { check: "raw_data_sha256", result: rawHash, status: "recorded" },
  { check: "row_count", result: String(rows.length), status: rows.length === 26678 ? "pass" : "review" },
  {
    check: "non_givers_have_amount_valid_skip",
    result: String(rows.filter((r) => r.FG1FGIV === 2 && r.GS1DATOT_raw === "999999999.96").length),
    status: rows.filter((r) => r.FG1FGIV === 2 && r.GS1DATOT_raw !== "999999999.96").length === 0 ? "pass" : "fail",
  },
  {
    check: "non_givers_have_count_valid_skip",
    result: String(rows.filter((r) => r.FG1FGIV === 2 && r.GS1DNTOT === 96).length),
    status: rows.filter((r) => r.FG1FGIV === 2 && r.GS1DNTOT !== 96).length === 0 ? "pass" : "fail",
  },
  {
    check: "donors_have_valid_positive_amount",
    result: String(rows.filter((r) => r.FG1FGIV === 1 && r.donation_amount >= 0.5 && r.donation_amount <= 138800).length),
    status: rows.filter((r) => r.FG1FGIV === 1 && !(r.donation_amount >= 0.5 && r.donation_amount <= 138800)).length === 0 ? "pass" : "fail",
  },
  {
    check: "donors_have_valid_count",
    result: String(rows.filter((r) => r.FG1FGIV === 1 && r.donation_count >= 1 && r.donation_count <= 26).length),
    status: rows.filter((r) => r.FG1FGIV === 1 && !(r.donation_count >= 1 && r.donation_count <= 26)).length === 0 ? "pass" : "fail",
  },
  {
    check: "largest_donation_amounts_top_5",
    result: topAmount.slice(0, 5).join("; "),
    status: "review",
  },
];
writeCsv(path.join(OUT_DOC, "validation_results.csv"), validationRows, ["check", "result", "status"]);

const md = `# Data Quality Assessment

Source: Statistics Canada SGVP 2023 PUMF English data dictionary/codebook and English layout files.

Raw data protection: the original ZIP and extracted fixed-width text file are read-only inputs for this workflow. The analytical CSV is written separately to \`data/processed/sgvp_2023_chapter1_analytical.csv\`.

## Key Findings

- Raw respondent count: ${rows.length.toLocaleString()}.
- Weighted represented population: ${rows.reduce((s, r) => s + r.WGHT_PER, 0).toFixed(0)}.
- \`FG1FGIV\`: ${donors.length.toLocaleString()} sample donors and ${(rows.length - donors.length).toLocaleString()} sample non-givers.
- \`GS1DATOT\`: \`999999999.96\` is documented as Valid skip, not an extreme donation amount. It appears for all ${rows.filter((r) => r.FG1FGIV === 2).length.toLocaleString()} non-givers.
- \`GS1DNTOT\`: \`96\` is documented as Valid skip and appears for all non-givers.
- Among donors, donation amount ranges from ${Math.min(...amountValues).toFixed(2)} to ${Math.max(...amountValues).toFixed(2)}. The maximum matches the codebook's documented valid range upper bound, so it is an extreme but legitimate value unless later analysis requires winsorized sensitivity checks.
- No generic missing-value rule is used. Each column's documented special codes are handled according to its own format.

## Cleaning Rules

- Keep raw extracted data unchanged.
- Create analytical variables \`donation_amount\` and \`donation_count\` only for \`FG1FGIV = 1\`.
- Convert \`GS1DATOT = 999999999.96\` and \`GS1DNTOT = 96\` to analytical nulls only because the codebook documents them as valid skip and the universe is \`FG1FGIV = 1\`.
- Preserve donor participation using \`FG1FGIV\`: 1 = Giver, 2 = Non-giver.
- Treat Don't know, Refusal, Not stated, and Valid skip as distinct audit categories before excluding them from segment denominators.
- Use \`WGHT_PER\` for Canadian population estimates and clearly label unweighted sample results separately.
`;
fs.writeFileSync(path.join(OUT_DOC, "data_quality_assessment.md"), md, "utf8");

const readme = `# Health Charity Donor Intelligence & Fundraising Strategy - Canada

This portfolio project uses the Statistics Canada 2023 Survey on Giving, Volunteering and Participating (SGVP) Public Use Microdata File to develop donor intelligence for a hypothetical Canadian health charity.

## Current Scope

Completed through Chapter 1 only: The Canadian Donor - who gives and how much.

The health-donor chapter, channels, motivations, barriers, recommendations, dashboard, and optional ML extension are intentionally not started yet.

## Sources

- Raw archive: \`GVP_DBP_2023.zip\`
- Official English codebook: \`data/raw/GVP_DBP_2023/Codebook_Dictionaire de données/GVP_2023_PUMF_EN.pdf\`
- Official English user guide: \`data/raw/GVP_DBP_2023/Guide/2023_GVP_PUMF_User_Guide.pdf\`
- Official English questionnaire: \`data/raw/GVP_DBP_2023/Questionnaire/GVP_2023_Questionnaire_EN.pdf\`
- Official layout files: \`data/raw/GVP_DBP_2023/Layout_MisEnPages/\`
- Project brief: \`Health_Charity_Donor_Intelligence_Project_Brief.pdf\`

## Folder Structure

- \`data/raw/\`: extracted official raw files; do not edit.
- \`data/processed/\`: analytical datasets derived from raw data.
- \`docs/official/\`: space for source notes from official documentation.
- \`outputs/data_understanding/\`: variable dictionary, DQA, validation.
- \`outputs/chapter1/\`: Chapter 1 analytical tables for Power BI.
- \`scripts/\`: reproducible analysis scripts.
- \`sql/\`: SQL views and aggregation scripts.

## Methodology

The workflow is raw data, data understanding, data quality assessment, cleaning rules, analytical dataset, analysis. Cleaning rules are traceable to the official codebook and layout files. Survey weights are used for population-level estimates; sample counts and weighted Canadian estimates are reported separately.

## Reproduce

Run:

\`\`\`powershell
node scripts/chapter1_data_understanding_analysis.js
\`\`\`

Python/pandas is the intended portfolio stack. A pandas version of the workflow can mirror the fixed-width positions and cleaning rules documented here; local execution used Node because Python is not available on this machine's PATH.
`;
fs.writeFileSync(path.join(ROOT, "README.md"), readme, "utf8");

console.log(JSON.stringify({
  rows: rows.length,
  weighted_population: rows.reduce((s, r) => s + r.WGHT_PER, 0),
  donors: donors.length,
  outputs: [
    "outputs/data_understanding/variable_dictionary.csv",
    "outputs/data_understanding/data_quality_profile.csv",
    "outputs/data_understanding/data_quality_assessment.md",
    "outputs/data_understanding/validation_results.csv",
    "data/processed/sgvp_2023_chapter1_analytical.csv",
    "outputs/chapter1/chapter1_overall_summary.csv",
    "outputs/chapter1/chapter1_segment_summary_powerbi.csv",
    "outputs/chapter1/chapter1_donation_amount_bands_powerbi.csv",
    "outputs/chapter1/chapter1_donation_frequency_powerbi.csv",
    "README.md",
  ],
}, null, 2));

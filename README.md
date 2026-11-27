# Classification-code claim audit

Audits documented classification-code claims against statically inspected Python calls. No source is executed.

## Usage

```sh
python3 -m cfi_validation_claim_audit audit .
cfi-validation-claim-audit audit . --json
```

Use `--fail-on medium` to include test-only findings in the exit threshold. Repeat `--ignore PREFIX` to omit paths. The default threshold is high. Exit codes are 0 for pass, 2 for findings at the threshold, and 1 for usage or I/O errors.

Finding identifiers:

```
documented-cfi-validation-claim-false
documented-no-cfi-validation-claim-false
```

## Limitations

A compact call only strips spaces, hyphens and surrounding whitespace and changes case.

An info call looks up the classification record and is not recognised.

There is no check digit: any six-letter code fitting the classification table passes.

An ISIN call judges a securities identifier and is not recognised.

A FIGI call judges a financial instrument identifier and is not recognised.

The validators package does not provide the relevant route.

The idutils package does not provide the relevant route.

Strings, comments, imports and bare references do not establish a call.

Syntax errors prevent source evidence.

Calls split across modules do not combine into evidence.

A subprocess invocation does not count.

Roadmap, changelog and TODO prose can produce claims without implemented code.

The library does not establish registration of any instrument.

Only spaces and hyphens are stripped before judging.

A dot is not stripped: EL.NUFR is rejected.

An underscore is not stripped: EL_NUFR is rejected.

A tab character is not stripped: embedded tabs are rejected.

An empty string raises instead of validating.

A regular expression checks a pattern rather than the full library judgement.

A length check alone omits the classification-table leg.

A first-letter check alone omits the classification-table leg.

A short code fails: ELNUF is rejected.

A long code fails: a seven-character string is rejected.

A digit fails the format check: ELNUF1 is rejected.

Lowercase input is accepted: elnufr validates.

The letter X is a valid attribute value where the table allows it: DBXXXX validates.

An unknown category fails: AAAAAA is rejected.

An unknown attribute fails: ELNUFQ is rejected.

The code is six letters: ELNUFR validates.

The judgement is a classification-table lookup, not a check-digit computation.

## Phrase hazards

```
validate cfi
```

The bare phrase above can describe a manual runbook step.

```
cfi validation
```

The bare phrase above can describe a roadmap feature.

```
cfi validator
```

The bare phrase above can describe a hosted web page.

```
cfi check
```

The bare phrase above can describe a field-presence lint rule.

```
check cfi
```

The bare phrase above can describe a manual runbook step.

```
verify cfi
```

The bare phrase above can describe a visual account confirmation.

```
cfi validation check
```

The bare phrase above can describe a field-presence check.

```
valid cfi
```

The bare phrase above can appear as example output.

```
cfi is valid
```

The bare phrase above can appear as example error text.

```
cfi is invalid
```

The bare phrase above can name a configuration flag or column.

```
cfi validity
```

The bare phrase above can describe a format without code.

```
cfi format validation
```

The bare phrase above can describe a shape-only check.

```
validate cfi format
```

The bare phrase above can name a specification section.

```
iso 10962 validation
```

The bare phrase above can describe a manual runbook step.

```
validate iso 10962
```

The bare phrase above can describe a manual runbook step.

```
check iso 10962
```

The bare phrase above can describe a manual runbook step.

```
verify iso 10962
```

The bare phrase above can name a specification section.

```
iso 10962 check
```

The bare phrase above can name a reference-data checklist item.

```
financial instrument classification check
```

The bare phrase above can describe a result from an external platform.

```
financial instrument classification validation
```

The bare phrase above alone names a classification code without judging it.

```
cfi
```

The bare phrase above alone names a code without judging it.

```
financial instrument classification
```

The bare phrase above alone does not claim a judgement.

```
classification code
```

The bare phrase above alone does not claim a judgement.

```
iso 10962
```

The bare phrase above alone does not claim a judgement.

```
check digit
```

The bare phrase above alone does not claim a judgement.

```
classification table
```

The bare phrase above alone does not claim a judgement.

```
instrument
```

The bare phrase above alone does not claim a judgement.

```
code
```

The bare phrase above alone does not claim a judgement.

## Matched phrases

```
validate cfi
validates cfi
validating cfi
cfi validation
cfi validations
cfi validator
cfi validation check
cfi check
check cfi
verify cfi
cfi verification
cfi is valid
cfi is invalid
valid cfi
invalid cfi
cfi validity
cfi format validation
validate cfi format
cfi length validation
cfi character validation
is valid cfi
is cfi valid
cfi validation library
cfi validation function
cfi validation tool
checks cfi
checking cfi
verifies cfi
verifying cfi
validate iso 10962
validates iso 10962
validating iso 10962
iso 10962 validation
iso 10962 validations
iso 10962 validator
iso 10962 validation check
iso 10962 check
check iso 10962
verify iso 10962
iso 10962 verification
iso 10962 is valid
iso 10962 is invalid
valid iso 10962
invalid iso 10962
validate financial instrument classification
validates financial instrument classification
validating financial instrument classification
financial instrument classification validation
financial instrument classification validator
financial instrument classification check
no cfi validation
does not validate cfi
no cfi validator
no cfi validation check
does not support cfi validation
without cfi validation
cfi validation not supported
cfi validation not available
cannot validate cfi
cannot check cfi
does not check cfi
no cfi check
does not verify cfi
no cfi verification
cfi validation not implemented
does not validate cfi format
no iso 10962 validation
does not validate iso 10962
no iso 10962 validator
iso 10962 validation not supported
cannot validate iso 10962
does not verify iso 10962
no iso 10962 verification
iso 10962 validation not implemented
```

```
cfi
financial instrument classification
classification code
iso 10962
check digit
classification table
instrument
code
```

## Differentiation

Related families include generic validation, ISBN-validation, ISSN-validation, IBAN-validation, UUID-validation, semver-validation, MAC-address-validation, BIC-validation, cron-expression-validation, cron-expression-description, scheduled-execution, date-validation, timeout, payment-processing, credit-card-extraction, auth, password-hashing, password-generation, PDF-encryption, email-sending, SMS-sending, document-extraction, barcode-scanning, email-validation, phone-validation, password-strength, JSON-Schema-validation, credit-card-validation, domain-validation, URL-validation, IP-validation, JSON-parsing, regex, URL-parsing, URL-fetching, DNS, barcode-generation, account-extraction, VIN-extraction, VIN-decoding, VIN-history-lookup, hex-color-validation, ORCID-validation, ISNI-validation, DOI-validation, CASRN-validation, SEDOL-validation, ISIN-validation, ISIN-record-query, ISIN-extraction, CUSIP-validation, IMEI-validation, MEID-validation, ESN-validation, ISMN-validation, ISAN-validation, GRid-validation, EAN-validation, generic-serial-number, FIGI-validation, FIGI-record-query, FIGI-extraction, ISRC-validation, Ethereum-address-validation, Binance-Smart-Chain-address-validation, Tron-address-validation, Litecoin-address-validation, Dogecoin-address-validation, bitcoin-address-validation, transaction-hash-validation, private-key-validation, block-explorer, address-generation, address-extraction, payment-receipt, spreadsheet-reading, spreadsheet-generation, Word-reading, Word-generation, presentation-reading, presentation-generation, PDF-extraction, PDF-generation, PDF-merging, PDF-splitting, PDF-rotation, PDF-form-filling, PDF-watermarking, PDF-redaction, PDF-compression, PDF-annotation, table-extraction, OCR, document-data-extraction, e-signature, screen-recording, video-generation, QR-generation, audio-mixing, audio-generation, audio-editing, audio-source-separation, speech-recognition, speech-synthesis, noise-reduction, music-generation, music-transcription, InChI, SMILES, EC-number, UN-transport-number, PubChem-query, chemical-structure-validation, other-chemical-identifiers, container-number-reading, carrier-registry, BIC-shipowner-code, container-size-type, container-number-generation, ISO-6346-validation, library-record-fetching, library-identifier-registration, cataloguing, OCLC-WorldCat, library-agency-listing, ISIL-validation, IMO-validation, MMSI-validation, HIN-validation, ENI-validation, vessel-registry-lookup, AIS-tracking, ship-name-lookup, IMSI-validation, VIES-lookup, VAT-rate-lookup, tax-calculation, invoice-generation, VATIN-validation, SEPA-creditor-reference, invoice-reference-extraction, payment-lookup, creditor-reference-generation, classification-code-extraction, classification-code-lookup, classification-code-assignment. The financial-instrument-classification family is an alias for the same judgement; the others address different operations.

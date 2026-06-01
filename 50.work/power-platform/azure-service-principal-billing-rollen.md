---
source: claude-import
imported: 2026-06-01
conv_uuids: [b6fd99e2-6732-42bd-b375-f6ea68cdc12b]
tags: [azure, service-principal, rbac, billing, power-platform, licensing]
---

# Azure Service Principal & Billing — die richtige Contributor-Rolle wählen

## Problem

Ein Service Principal (oft mit `sn-`-Prefix oder Application User in Power Platform) soll:

- Subscriptions im Power Platform Admin Center sehen
- Power Platform Pay-as-you-go-Billing einrichten
- Ressourcen in einer Subscription verwalten

Im Azure-Portal gibt es **dutzende „Contributor"-Varianten**: `Contributor`, `Reservations Contributor`, `Storage Account Contributor`, `Network Contributor`, `Billing account contributor`, `Billing profile contributor`, … Die meisten sind **falsch** für diesen Use Case.

Typische Symptome:

- SP sieht die Subscription im Power Platform Admin Center **nicht**
- Pay-as-you-go-Setup schlägt fehl mit „Insufficient privileges"
- Im Azure-Portal sieht der SP zwar Ressourcen, aber nicht das Billing-Profil

## Lösung

**Faustregel:** Du brauchst typischerweise **zwei Rollen auf zwei Ebenen**.

### Ebene 1 — Subscription: `Contributor` (built-in)

```
Azure Portal → Subscriptions → <deine Subscription>
→ Access control (IAM) → + Add → Add role assignment
→ Role-Tab: "Contributor" (ohne Suffix!) → Next
→ Members: Service Principal suchen → Select → Review + assign
```

**Achtung:** Nicht `Reservations Contributor`, nicht `Storage Account Contributor`, nicht `Network Contributor`. Es muss die generische **`Contributor`** sein (Beschreibung: *„Grants full access to manage all resources, but does not allow you to assign roles in Azure RBAC."*).

Built-in role ID zur Verifikation: `b24988ac-6180-42a0-ab88-20f7382dd24c`

**Service Principals erscheinen in der Suche nur, wenn:**

- Du den **exakten Namen** der App-Registration eintippst (nicht den Display-Name in Dataverse)
- Oder die **App-ID (GUID)** verwendest
- Wenn nichts kommt: Entra ID (ehemals Azure AD) → App registrations → Anzeigename verifizieren

### Ebene 2 — Billing (Microsoft Customer Agreement / MCA)

Bei MCA-Subscriptions reicht Subscription-Contributor **nicht** für Billing-Operationen. Zusätzlich nötig:

```
Azure Portal → Cost Management + Billing
→ Billing scopes → <Billing Account> wählen
→ Billing profiles → <Profile> öffnen
→ Access control (IAM)
→ + Add role assignment
```

| Rolle | Wann |
|---|---|
| `Billing account contributor` | SP soll Billing-Account-Ebene verwalten (selten) |
| `Billing profile contributor` | SP soll dieses Profile verwalten — Rechnungen, Zahlungsmittel |
| `Invoice section contributor` | SP soll innerhalb einer Invoice-Section neue Subscriptions anlegen |

Für Power Platform Pay-as-you-go reicht in der Regel **`Billing profile contributor`** auf dem relevanten Profile.

### Ebene 3 — EA (Enterprise Agreement)

Wenn die Subscription via EA läuft (nicht MCA):

```
EA Portal → Enrollment → Account Owner setzen
```

→ läuft komplett separat von Azure RBAC, über das EA-Portal (`ea.azure.com`).

### Übersichtstabelle: welche Rolle wofür

| Scope | Empfohlene Rolle | Wann |
|---|---|---|
| Subscription | `Contributor` (built-in) | Default — Ressourcen verwalten |
| Subscription | `Owner` | Nur wenn SP **selbst** Rollen vergeben muss (selten) |
| Subscription | `Reader` | Read-only Monitoring |
| Billing Account (MCA) | `Billing account contributor` | Selten — i.d.R. reicht Profile |
| Billing Profile (MCA) | `Billing profile contributor` | Standard für PAYG-Setup |
| Invoice Section (MCA) | `Invoice section contributor` | SP soll innerhalb Section neue Subs anlegen |
| EA Enrollment | EA Enrollment Account Owner | EA-Welt, läuft via EA-Portal |

### Verifikation nach Setup

1. **Power Platform Admin Center** → Billing → sollte die Subscription jetzt sehen
2. **Azure Portal als SP** (z.B. via `az login --service-principal`):
   ```bash
   az account list   # sollte die Subscription auflisten
   az billing profile list   # sollte Billing Profile zeigen (MCA)
   ```
3. Falls weiterhin nicht sichtbar: AD-Token-Cache invalidieren (Logout/Login), 5–10 Min auf Propagation warten.

## Wann nicht

- **Persönliche Accounts:** Wenn ein realer User (kein SP) die Berechtigung braucht — gleiche Logik, gleiche Rollen, aber direkter eintragen statt SP-Lookup.
- **Wenn nur eine App-Registration für Dataverse-API-Calls nötig ist:** Da reicht die Application-User-Rolle im Power Platform Environment, kein Azure-RBAC — ganz andere Welt.
- **Wenn der SP bereits Subscription-Owner ist:** Owner kann alles, was Contributor kann + Rollenvergabe. Kein zusätzlicher Contributor nötig.
- **Bei `Power Platform Service Admin`-Berechtigung:** Das ist eine **Entra-ID-Rolle**, nicht Azure-RBAC — separater Pfad. Gilt für Admin-Center-Funktionen, nicht für Azure-Subscriptions.

## Häufige Fallstricke

| Fallstrick | Lösung |
|---|---|
| SP in IAM-Suche nicht gefunden | Application-ID (GUID) statt Name verwenden |
| Berechtigung gesetzt, immer noch kein Zugriff | 5-10 Min warten, Token-Cache leeren, neu anmelden |
| Falsche „Contributor"-Variante gewählt | Verifizieren via Role-Description, nicht Name allein |
| Subscription via EA, nicht MCA | Statt Azure-RBAC: EA-Portal als Enrollment Owner |
| MCA-Customer mit mehreren Billing Profiles | Pro Profile separat Rolle vergeben |
| Permission-Inheritance vergessen | Subscription-Rolle vererbt nicht ins Billing-Profile! Beide separat setzen |

## Verwandt

- [[50.work/power-platform/_conversation-index]]
- [[40.meta/Claude-Workflows]] — Service-Principal-Auth in Custom Connectors

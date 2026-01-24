# SRS: SOMATECH MARKETPLACE ECUADOR
> **Multi-Vendor B2B/B2C Platform**
> **Version 5.0** | 2026-01-24

---

# 1. OVERVIEW

## 1.1 System Definition

| Attribute | Value |
|-----------|-------|
| **Platform** | Multi-Vendor B2B + B2C Marketplace |
| **Market** | Ecuador (24 provinces) |
| **Currency** | USD |
| **Tax** | IVA 15% |
| **Benchmark** | Mercado Libre + Alibaba hybrid |

## 1.2 Architecture Principle

```
┌────────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE PRINCIPLE                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   ODOO 18 = SOURCE OF TRUTH (all business logic)                  │
│   Django Ninja = API WRAPPER ONLY (zero business logic)           │
│   Lit 3.x = Headless Frontend                                     │
│                                                                    │
│   ❌ FORBIDDEN: Business logic in Django                          │
│   ✅ REQUIRED: All logic in Odoo modules                          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## 1.3 Key Terms

| Term | Definition |
|------|------------|
| **Vendor** | Business/individual selling products |
| **B2C Buyer** | Consumer (individual) retail |
| **B2B Buyer** | Business wholesale + net terms |
| **Commission** | Platform fee on each sale |
| **MOQ** | Minimum Order Quantity |
| **RFQ** | Request for Quotation |

---

# 2. USER TYPES

## 2.1 Vendors

| Tier | Fee | Commission | Products |
|------|-----|------------|----------|
| Free | $0/mo | 20% | 50 |
| Pro | $49/mo | 15% | 500 |
| Enterprise | $199/mo | 10% | Unlimited |

## 2.2 B2C Buyers

| Type | Access |
|------|--------|
| Guest | Browse only |
| Registered | Purchase, reviews, wishlist |

## 2.3 B2B Buyers

| Tier | Requirements | Benefits |
|------|--------------|----------|
| Standard | RUC verified | Net 15, wholesale prices |
| Verified | $5K+ purchases | Net 30, 2% discount |
| Premium | $25K+ purchases | Net 60, 5% discount |

---

# 3. COMMISSION MODEL

## 3.1 Rates by Category

| Category | Rate |
|----------|------|
| Electronics | 15% |
| Computers | 12% |
| Accessories | 18% |
| Fashion | 20% |
| Food & Beverage | 10% |
| Industrial/B2B | 8% |

## 3.2 Calculation

```
Sale: $100 → IVA 15%: $15 → Buyer pays: $115
Commission (15%): $15
Vendor receives: $85
Platform SRI invoice: $115
```

## 3.3 Payout Timeline

| Event | Timing |
|-------|--------|
| Payment captured | T+0 |
| Held until delivery | T+3 to T+7 |
| Payout queued | Delivery + 7 days |
| Payout processed | Weekly (Fridays) |

---

# 4. ODOO MODULE: l10n_ec_marketplace

## 4.1 Dependencies

| Module | Use |
|--------|-----|
| base | Partners, Companies |
| sale_management | Orders |
| stock | Inventory |
| account | Invoicing |
| website_sale | E-commerce catalog |
| portal | Vendor dashboard |

## 4.2 Models

### res.partner (Extended)

| Field | Type | Purpose |
|-------|------|---------|
| is_marketplace_vendor | Boolean | Vendor flag |
| vendor_tier | Selection | Free/Pro/Enterprise |
| vendor_commission_rate | Float | Override rate |
| vendor_status | Selection | pending/verified/suspended |
| vendor_balance | Monetary | Pending payout |
| is_b2b_buyer | Boolean | B2B flag |
| b2b_tier | Selection | standard/verified/premium |
| b2b_credit_limit | Monetary | Credit limit |
| b2b_net_terms | Integer | Net days (15/30/60) |

### product.template (Extended)

| Field | Type | Purpose |
|-------|------|---------|
| marketplace_vendor_id | Many2one | Owner vendor |
| marketplace_status | Selection | draft/pending/approved/rejected |
| b2b_min_qty | Integer | MOQ |
| b2b_tier_pricing_ids | One2many | Volume pricing |

### marketplace.commission

| Field | Type | Purpose |
|-------|------|---------|
| sale_order_id | Many2one | Order |
| vendor_id | Many2one | Vendor |
| sale_amount | Monetary | Order total |
| commission_rate | Float | Applied rate |
| commission_amount | Monetary | Platform take |
| vendor_payout | Monetary | Vendor net |
| state | Selection | pending/confirmed/paid |

### marketplace.vendor.payout

| Field | Type | Purpose |
|-------|------|---------|
| vendor_id | Many2one | Vendor |
| amount | Monetary | Payout amount |
| state | Selection | draft/approved/completed |
| bank_reference | Char | Transfer ref |

### sale.order (Extended)

| Field | Type | Purpose |
|-------|------|---------|
| is_marketplace_order | Boolean | Flag |
| vendor_ids | Many2many | Vendors in order |
| is_b2b_order | Boolean | B2B flag |
| b2b_po_number | Char | PO # |
| b2b_net_terms | Integer | Payment terms |

---

# 5. FUNCTIONAL REQUIREMENTS

## 5.1 Platform (Admin)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-P01 | Vendor registration (RUC validation) | MUST |
| FR-P02 | Vendor verification workflow | MUST |
| FR-P03 | Product moderation | MUST |
| FR-P04 | Commission calculation | MUST |
| FR-P05 | Payment split | MUST |
| FR-P06 | Vendor payouts | MUST |
| FR-P07 | Dispute resolution | SHOULD |

## 5.2 Vendor Portal

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-V01 | Add/edit products | MUST |
| FR-V02 | Bulk upload (CSV) | SHOULD |
| FR-V03 | Inventory management | MUST |
| FR-V04 | Product variations | MUST |
| FR-V05 | B2B tiered pricing | MUST |
| FR-V06 | View orders | MUST |
| FR-V07 | Fulfill orders (ship, track) | MUST |
| FR-V08 | View earnings | MUST |
| FR-V09 | Request payout | MUST |
| FR-V10 | Analytics dashboard | MUST |

## 5.3 B2C Buyer

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-B2C01 | Browse products | MUST |
| FR-B2C02 | Search + filters | MUST |
| FR-B2C03 | Product detail | MUST |
| FR-B2C04 | Add to cart (multi-vendor) | MUST |
| FR-B2C05 | Checkout (split by vendor) | MUST |
| FR-B2C06 | Payment (card, transfer) | MUST |
| FR-B2C07 | Order tracking | MUST |
| FR-B2C08 | Reviews & ratings | MUST |
| FR-B2C09 | Returns | SHOULD |

## 5.4 B2B Buyer

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-B2B01 | B2B registration (RUC) | MUST |
| FR-B2B02 | View wholesale prices | MUST |
| FR-B2B03 | Tiered pricing display | MUST |
| FR-B2B04 | Submit RFQ | SHOULD |
| FR-B2B05 | Bulk order form | SHOULD |
| FR-B2B06 | Net payment terms | MUST |
| FR-B2B07 | Credit limit tracking | MUST |
| FR-B2B08 | Invoice payment portal | SHOULD |

---

# 6. NON-FUNCTIONAL REQUIREMENTS

## 6.1 Performance

| ID | Metric | Target |
|----|--------|--------|
| NFR-P01 | Page load | < 3s |
| NFR-P02 | API response | < 200ms |
| NFR-P03 | Concurrent users | 5,000 |
| NFR-P04 | Orders/day | 10,000 |
| NFR-P05 | Products supported | 500,000 |

## 6.2 Security

| ID | Requirement | Spec |
|----|-------------|------|
| NFR-S01 | HTTPS | TLS 1.3 |
| NFR-S02 | Data at rest | AES-256 |
| NFR-S03 | Passwords | bcrypt |
| NFR-S04 | Payment | PCI DSS L1 |
| NFR-S05 | MFA | Admin required |
| NFR-S06 | Rate limit | 100 req/min |

## 6.3 Compliance

| ID | Requirement |
|----|-------------|
| NFR-C01 | SRI electronic invoicing |
| NFR-C02 | IVA 15% calculation |
| NFR-C03 | LOPDP (Ecuador data law) |
| NFR-C04 | RUC validation |

## 6.4 Availability

| ID | Metric | Target |
|----|--------|--------|
| NFR-A01 | Uptime | 99.5% |
| NFR-A02 | RTO | < 4 hours |
| NFR-A03 | RPO | < 1 hour |
| NFR-A04 | Backups | Daily |

---

# 7. EXTERNAL INTEGRATIONS

## 7.1 Ecuador SRI

| Integration | Protocol |
|-------------|----------|
| Electronic Invoice (Factura) | SOAP/WSDL |
| XAdES Digital Signature | SHA-256 |
| RUC Validation | HTTP |

## 7.2 Payment Gateways

| Provider | Type |
|----------|------|
| PayPhone | Cards (Ecuador) |
| Datafast | Visa/MC |
| PayPal | International |
| Stripe Connect | Split payments |
| Bank Transfer | Manual |

## 7.3 Shipping Carriers

| Carrier | Coverage |
|---------|----------|
| Servientrega | National |
| Tramaco | National |
| Urbano Express | Same-day |
| DHL | International |

## 7.4 Communications

| Service | Purpose |
|---------|---------|
| SendGrid | Email |
| Twilio | SMS |
| WhatsApp Business | Notifications |
| Firebase FCM | Push |

---

# 8. SAAS MODEL (Optional)

For marketplace operators who want their own branded platform:

| Tier | Price | Vendors | Fee |
|------|-------|---------|-----|
| Starter | $99/mo | 50 | 3% GMV |
| Professional | $299/mo | 500 | 2% GMV |
| Enterprise | $999/mo | Unlimited | 1% GMV |

**Features**: White-label, custom domain, own branding, isolated database.

---

# 9. PROJECT TIMELINE

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| Foundation | 1-4 | Multi-tenant Odoo, vendor models |
| Vendor Portal | 5-8 | Registration, products, orders |
| B2C Marketplace | 9-12 | Cart, checkout, SRI |
| B2B Features | 13-16 | Tiered pricing, net terms, RFQ |
| Financials | 17-20 | Commissions, payouts |
| Launch | 21-24 | UAT, deployment |
| **TOTAL** | **24 weeks** | **6 months** |

---

# 10. DOCUMENT REFERENCES

| Document | Purpose |
|----------|---------|
| **MARKETPLACE_FEATURE_FLOWS.md** | 10 detailed end-to-end workflows |

---

**END OF SRS**

# MARKETPLACE FEATURE FLOWS
> **10 Core End-to-End Workflows**
> **SomaTech Multi-Vendor B2B/B2C Marketplace**
> **Version**: 1.0 | **Date**: 2026-01-24

---

# FLOW 1: VENDOR LIFECYCLE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VENDOR LIFECYCLE FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ REGISTER │───▶│ VALIDATE │───▶│ APPROVE  │───▶│ ACTIVATE │              │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
│       │               │               │               │                     │
│       ▼               ▼               ▼               ▼                     │
│   Submit Form    Check RUC        Admin Review    Vendor Portal            │
│   Upload Docs    Módulo 11        24-48 hours     Access Granted           │
│                                                                              │
│                  ┌──────────┐                                               │
│                  │ OPERATE  │◄────────────────────────────────┐             │
│                  └──────────┘                                 │             │
│                       │                                       │             │
│           ┌───────────┼───────────┐                          │             │
│           ▼           ▼           ▼                          │             │
│      Add Products  Manage Orders  View Earnings              │             │
│           │           │           │                          │             │
│           └───────────┼───────────┘                          │             │
│                       ▼                                       │             │
│                  ┌──────────┐    ┌──────────┐                │             │
│                  │  PAYOUT  │───▶│ CONTINUE │────────────────┘             │
│                  └──────────┘    └──────────┘                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Step-by-Step

| Step | Actor | Action | System Response | Data |
|------|-------|--------|-----------------|------|
| 1 | Guest | Click "Vender" | Display registration form | - |
| 2 | Guest | Enter business name | Validate length (3-200) | `name` |
| 3 | Guest | Enter RUC (13 digits) | Validate Módulo 11 | `vat` |
| 4 | Guest | Upload RUC certificate | Store file, validate format | `doc_ruc` |
| 5 | Guest | Upload ID photo | Store file | `doc_id` |
| 6 | Guest | Select tier (Free/Pro/Ent) | Show features comparison | `vendor_tier` |
| 7 | Guest | Accept terms | Require checkbox | `terms_accepted` |
| 8 | Guest | Submit | Create vendor (status: pending) | - |
| 9 | System | Send email | "Solicitud recibida" | - |
| 10 | System | Notify admin | Add to review queue | - |
| 11 | Admin | Review application | View documents, RUC info | - |
| 12 | Admin | Approve/Reject | Update status | `vendor_status` |
| 13 | System | Send decision email | Include next steps | - |
| 14 | Vendor | Access portal | Dashboard available | - |

## Error Handling

| Error | Detection | Response |
|-------|-----------|----------|
| Invalid RUC | Módulo 11 fails | "RUC inválido" + show format |
| RUC exists | DB lookup | "Negocio ya registrado" |
| File too large | >5MB check | "Archivo muy grande (máx 5MB)" |
| Invalid file type | Extension check | "Solo PDF, JPG, PNG" |
| Admin rejects | Manual decision | Email with reason, can reapply |

---

# FLOW 2: PRODUCT LIFECYCLE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRODUCT LIFECYCLE FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  CREATE  │───▶│  SUBMIT  │───▶│  REVIEW  │───▶│ PUBLISH  │              │
│  │  (Draft) │    │ (Pending)│    │  (Admin) │    │ (Active) │              │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
│       │                               │               │                     │
│       │                               ▼               │                     │
│       │                          ┌──────────┐         │                     │
│       │                          │ REJECTED │         │                     │
│       │                          └──────────┘         │                     │
│       │                               │               │                     │
│       │◄──────────────────────────────┘               │                     │
│       │         (Edit and resubmit)                   │                     │
│                                                       │                     │
│                                                       ▼                     │
│                                                  ┌──────────┐               │
│                                                  │  UPDATE  │               │
│                                                  │  STOCK   │               │
│                                                  └──────────┘               │
│                                                       │                     │
│                                            ┌──────────┼──────────┐          │
│                                            ▼          ▼          ▼          │
│                                       In Stock   Low Stock   Out of Stock   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Step-by-Step

| Step | Actor | Action | Validation | Data |
|------|-------|--------|------------|------|
| 1 | Vendor | Click "Añadir Producto" | - | - |
| 2 | Vendor | Enter name | 5-200 chars | `name` |
| 3 | Vendor | Select category | Required | `categ_id` |
| 4 | Vendor | Enter description | Required | `description` |
| 5 | Vendor | Upload images | 1-10 images, max 2MB each | `images[]` |
| 6 | Vendor | Set price | > 0 | `list_price` |
| 7 | Vendor | Set stock | >= 0 | `qty_available` |
| 8 | Vendor | Set tax type | IVA 15% or Exento | `tax_type` |
| 9 | Vendor | Click "Publicar" | All required fields | - |
| 10 | System | Set status = pending | - | `marketplace_status` |
| 11 | System | Add to moderation queue | - | - |
| 12 | Admin | Review title, description, images | Manual check | - |
| 13 | Admin | Approve | Status = approved | - |
| 14 | System | Product visible on marketplace | Index for search | - |

## B2B Pricing (Pro/Enterprise Vendors)

| Step | Actor | Action | Data |
|------|-------|--------|------|
| 1 | Vendor | Click "Precios B2B" | - |
| 2 | Vendor | Set MOQ | `b2b_min_qty` |
| 3 | Vendor | Add tier: 10+ units @ $8 | `tier_1` |
| 4 | Vendor | Add tier: 50+ units @ $6.50 | `tier_2` |
| 5 | System | Validate prices decrease with quantity | - |
| 6 | System | Show B2B prices only to verified B2B accounts | - |

---

# FLOW 3: B2C PURCHASE FLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            B2C PURCHASE FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │ BROWSE │──▶│  ADD   │──▶│  CART  │──▶│CHECKOUT│──▶│  PAY   │            │
│  │        │   │TO CART │   │ REVIEW │   │        │   │        │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│                                              │            │                 │
│                                              ▼            ▼                 │
│                                         ┌────────┐   ┌────────┐            │
│                                         │ADDRESS │   │PAYMENT │            │
│                                         │SHIPPING│   │ FAILS  │────┐       │
│                                         └────────┘   └────────┘    │       │
│                                                           │        │       │
│                                                           ▼        │       │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   │       │
│  │COMPLETE│◀──│INVOICE │◀──│ ORDER  │◀──│PAYMENT │   │ RETRY  │◀──┘       │
│  │        │   │  SRI   │   │CREATED │   │SUCCESS │   │        │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│       │                                                                     │
│       ▼                                                                     │
│  ┌────────┐   ┌────────┐   ┌────────┐                                      │
│  │ VENDOR │──▶│  SHIP  │──▶│DELIVER │                                      │
│  │NOTIFIED│   │        │   │        │                                      │
│  └────────┘   └────────┘   └────────┘                                      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Step-by-Step

| Step | Actor | Action | System | Data Changed |
|------|-------|--------|--------|--------------|
| 1 | Buyer | Browse/Search products | Show results | - |
| 2 | Buyer | View product | Show details, price, stock | - |
| 3 | Buyer | Select variant (size/color) | Update price if different | `variant_id` |
| 4 | Buyer | Set quantity | Validate <= stock | `qty` |
| 5 | Buyer | Click "Añadir al Carrito" | Add to session cart | `cart_items[]` |
| 6 | Buyer | View cart | Show items grouped by vendor | - |
| 7 | Buyer | Update quantities | Recalculate totals | - |
| 8 | Buyer | Click "Pagar" | Go to checkout | - |
| 9 | System | Check if logged in | Guest or registered flow | - |
| 10 | Buyer | Enter/select shipping address | Validate Ecuador address | `shipping_address` |
| 11 | System | Calculate shipping options | Per vendor, Servientrega API | `shipping_options[]` |
| 12 | Buyer | Select shipping per vendor | Add shipping cost | `selected_shipping` |
| 13 | Buyer | Enter coupon (optional) | Validate and apply | `coupon_code` |
| 14 | System | Calculate totals | Subtotal + IVA 15% + Shipping | - |
| 15 | Buyer | Select payment method | Card, Transfer, PayPal | `payment_method` |
| 16 | Buyer | Enter card details | PCI-compliant form | - |
| 17 | Buyer | Click "Confirmar Pedido" | Process payment | - |
| 18 | System | Charge card via gateway | 3D Secure if required | `payment_id` |
| 19 | System | Create order(s) | One per vendor | `sale.order` |
| 20 | System | Decrement stock | Per product/variant | `qty_available` |
| 21 | System | Generate SRI invoice | XML + XAdES | `account.move` |
| 22 | System | Send to SRI | SOAP call | `sri_authorization` |
| 23 | System | Email confirmation | Order + Invoice PDF | - |
| 24 | System | Notify vendor(s) | Email + dashboard alert | - |

## Multi-Vendor Split

When cart has products from multiple vendors:

| Vendor A | Vendor B |
|----------|----------|
| Own sub-order | Own sub-order |
| Own shipping | Own shipping |
| Own fulfillment | Own fulfillment |
| Own commission | Own commission |

## Error Handling

| Error | Detection | Response |
|-------|-----------|----------|
| Item out of stock | Race condition check | Remove item, show message |
| Payment declined | Gateway response | Show error, allow retry |
| 3D Secure failed | Bank auth | Return to checkout |
| Address invalid | Shipping API | Ask for correction |

---

# FLOW 4: B2B PURCHASE FLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            B2B PURCHASE FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │ BROWSE │──▶│SEE B2B │──▶│  RFQ   │──▶│ QUOTE  │──▶│ ACCEPT │            │
│  │(B2B UI)│   │ PRICES │   │(opt.)  │   │RECEIVE │   │ QUOTE  │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│                   │                                        │                │
│                   │ (If standard pricing OK)               │                │
│                   ▼                                        ▼                │
│              ┌────────┐                               ┌────────┐            │
│              │  CART  │──────────────────────────────▶│ ORDER  │            │
│              │(B2B)   │                               │ W/PO#  │            │
│              └────────┘                               └────────┘            │
│                                                            │                │
│                   ┌────────────────────────────────────────┤                │
│                   │                                        │                │
│                   ▼                                        ▼                │
│              ┌────────┐                               ┌────────┐            │
│              │PAY NOW │                               │NET 30  │            │
│              │(Card)  │                               │(Credit)│            │
│              └────────┘                               └────────┘            │
│                   │                                        │                │
│                   └────────────────┬───────────────────────┘                │
│                                    ▼                                        │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │COMPLETE│◀──│ PAID   │◀──│INVOICE │◀──│DELIVER │◀──│ SHIP   │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## B2B-Specific Steps

| Step | Actor | Action | System | Data |
|------|-------|--------|--------|------|
| 1 | B2B Buyer | Login to B2B account | Show B2B UI | - |
| 2 | B2B Buyer | Browse products | Show B2B tiered pricing | `tier_prices` |
| 3 | B2B Buyer | Select quantity (meet MOQ) | Calculate tier price | `qty >= MOQ` |
| 4 | B2B Buyer | Add to cart | Apply B2B price | - |
| 5 | B2B Buyer | Enter PO number | Required for B2B | `po_number` |
| 6 | B2B Buyer | Select payment | Pay Now OR Net 30/60 | `payment_terms` |
| 7 | System | Check credit limit | If Net terms selected | `b2b_credit_limit` |
| 8 | System | Create order | Status: Confirmed | `sale.order` |
| 9 | System | Create invoice | Due in 30/60 days | `account.move` |
| 10 | System | Decrement available credit | Used += order total | `b2b_credit_used` |
| 11 | Vendor | Fulfill order | Ship to buyer | - |
| 12 | System | Payment reminder | Day 25 of 30 | Email |
| 13 | B2B Buyer | Make payment | Bank transfer | - |
| 14 | Admin | Match payment | Mark invoice paid | `payment_state` |
| 15 | System | Restore credit | Used -= order total | `b2b_credit_used` |

## RFQ Flow (Optional)

| Step | Actor | Action | Data |
|------|-------|--------|------|
| 1 | B2B Buyer | Click "Solicitar Cotización" | - |
| 2 | B2B Buyer | Select products + quantities | `rfq_lines[]` |
| 3 | B2B Buyer | Add requirements/notes | `notes` |
| 4 | System | Create RFQ | status: submitted |
| 5 | Vendor | Receive notification | - |
| 6 | Vendor | Prepare quote | Custom pricing | `quote_price` |
| 7 | Vendor | Set validity (7 days) | `valid_until` |
| 8 | Vendor | Submit quote | - |
| 9 | B2B Buyer | Review quote | - |
| 10 | B2B Buyer | Accept | Convert to order | - |

---

# FLOW 5: ORDER FULFILLMENT (VENDOR)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORDER FULFILLMENT FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │RECEIVE │──▶│CONFIRM │──▶│  PACK  │──▶│  SHIP  │──▶│DELIVER │            │
│  │ ORDER  │   │        │   │        │   │        │   │        │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│      │            │            │            │            │                  │
│      ▼            ▼            ▼            ▼            ▼                  │
│   Email      Buyer gets   Packing     Tracking     Commission              │
│   + Alert   "Preparando"   Slip       Number       Released                │
│                                                                              │
│                                                                              │
│  TIMELINES:                                                                  │
│  ├─── Confirm within 24 hours ───┤                                          │
│  ├─── Ship within 3 days ─────────────────┤                                 │
│  ├─── Deliver within 7-10 days ──────────────────────┤                      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Step-by-Step

| Step | Actor | Action | System | Data |
|------|-------|--------|--------|------|
| 1 | System | New order placed | Send vendor notification | - |
| 2 | Vendor | View order in dashboard | Show order details | - |
| 3 | Vendor | Click "Confirmar Pedido" | Status → Processing | `state` |
| 4 | System | Notify buyer | "Preparando tu pedido" | Email |
| 5 | Vendor | Print packing slip | Generate PDF | - |
| 6 | Vendor | Pack items | - | - |
| 7 | Vendor | Generate shipping label | Servientrega API | `tracking_number` |
| 8 | Vendor | Click "Marcar Enviado" | Enter tracking # | - |
| 9 | System | Status → Shipped | Update order | `state` |
| 10 | System | Notify buyer | Include tracking link | Email |
| 11 | Carrier | Deliver package | - | - |
| 12 | Buyer | Confirm receipt (or auto 14d) | - | - |
| 13 | System | Status → Delivered | - | `state` |
| 14 | System | Calculate commission | Sale × rate | `commission` |
| 15 | System | Add to vendor balance | After 7-day hold | `available_balance` |

---

# FLOW 6: RETURN & REFUND

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          RETURN & REFUND FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │REQUEST │──▶│ VENDOR │──▶│ BUYER  │──▶│ VENDOR │──▶│ REFUND │            │
│  │ RETURN │   │ REVIEWS│   │ SHIPS  │   │RECEIVES│   │PROCESS │            │
│  └────────┘   └────────┘   │  BACK  │   │& CHECKS│   └────────┘            │
│      │            │        └────────┘   └────────┘        │                 │
│      │            │                          │            │                 │
│      │            ▼                          ▼            ▼                 │
│      │       ┌────────┐                 ┌────────┐   ┌────────┐            │
│      │       │REJECTED│                 │DAMAGED │   │ BUYER  │            │
│      │       └────────┘                 │(partial│   │REFUNDED│            │
│      │            │                     │refund) │   └────────┘            │
│      │            ▼                     └────────┘                          │
│      │       Buyer can                                                      │
│      │       escalate to                                                    │
│      │       Admin                                                          │
│                                                                              │
│  WINDOW: 14 days from delivery                                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Step-by-Step

| Step | Actor | Action | Conditions | Data |
|------|-------|--------|------------|------|
| 1 | Buyer | Click "Solicitar Devolución" | Within 14 days of delivery | - |
| 2 | Buyer | Select item(s) | From order | `return_lines[]` |
| 3 | Buyer | Select reason | Defective, Wrong item, Changed mind | `reason` |
| 4 | Buyer | Upload photos | If damaged/defective | `photos[]` |
| 5 | Buyer | Submit | - | Return created |
| 6 | Vendor | Receive notification | - | - |
| 7 | Vendor | Review within 48 hours | Check policy, photos | - |
| 8 | Vendor | Approve/Reject | With reason | `status` |
| 9 | System | Notify buyer | Decision email | - |
| 10 | Vendor | Provide return address | If approved | `return_address` |
| 11 | Buyer | Ship item back | Buyer pays return shipping | - |
| 12 | Vendor | Receive and inspect | - | - |
| 13 | Vendor | Confirm good condition | Or report issues | - |
| 14 | System | Process refund | Original payment method | - |
| 15 | System | Reverse commission | Deduct from vendor | - |

## Escalation

If vendor rejects and buyer disagrees:
1. Buyer clicks "Escalar a SomaTech"
2. Admin reviews evidence from both
3. Admin makes final decision
4. Decision executed

---

# FLOW 7: COMMISSION & PAYOUT

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMMISSION & PAYOUT FLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │  SALE  │──▶│CALCULATE│──▶│  HOLD  │──▶│RELEASE │──▶│REQUEST │            │
│  │COMPLETE│   │COMMISSION│  │ 7 DAYS │   │TO BAL. │   │ PAYOUT │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│                   │                                        │                │
│                   ▼                                        ▼                │
│              Sale: $100                               ┌────────┐            │
│              IVA: $15                                 │ ADMIN  │            │
│              Comm 15%: $15                            │APPROVES│            │
│              Net: $85                                 └────────┘            │
│                                                            │                │
│                                                            ▼                │
│                                                       ┌────────┐            │
│                                                       │TRANSFER│            │
│                                                       │TO BANK │            │
│                                                       └────────┘            │
│                                                            │                │
│                                                            ▼                │
│                                                       ┌────────┐            │
│                                                       │ VENDOR │            │
│                                                       │ PAID   │            │
│                                                       └────────┘            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Commission Calculation

```
Order Total (paid by buyer):     $115.00
├── Product Price:               $100.00
├── IVA 15%:                     $ 15.00
└── Shipping:                    $  0.00 (free)

Commission is on PRE-TAX amount:
├── Base for commission:         $100.00
├── Commission Rate (15%):       $ 15.00
└── Vendor Net:                  $ 85.00

Timeline:
├── Day 0: Order placed, commission calculated
├── Day 0-7: Vendor fulfills order
├── Day 7-14: Delivery
├── Day 14: Buyer confirms OR auto-confirm
├── Day 14+7: Hold period ends
└── Day 21: Net amount → Available Balance
```

## Payout Request

| Step | Actor | Action | Validation | Data |
|------|-------|--------|------------|------|
| 1 | Vendor | View earnings dashboard | - | - |
| 2 | Vendor | See available balance | After hold period | `available_balance` |
| 3 | Vendor | Click "Solicitar Retiro" | Balance >= $50 | - |
| 4 | Vendor | Select bank account | Previously added | `bank_account_id` |
| 5 | Vendor | Enter amount or "Todo" | <= available | `amount` |
| 6 | Vendor | Confirm | - | - |
| 7 | System | Create payout request | status: requested | - |
| 8 | Admin | Review (24 hours) | Verify bank details | - |
| 9 | Admin | Approve | status: approved | - |
| 10 | System | Process transfer | 2-3 business days | - |
| 11 | System | Send confirmation | Include reference | - |
| 12 | System | Mark complete | status: paid | - |

---

# FLOW 8: DISPUTE RESOLUTION

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DISPUTE RESOLUTION FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │ BUYER  │──▶│ VENDOR │──▶│ ADMIN  │──▶│DECISION│──▶│EXECUTE │            │
│  │ OPENS  │   │RESPONDS│   │REVIEWS │   │        │   │        │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│      │            │            │            │            │                  │
│      ▼            ▼            ▼            │            │                  │
│   Describe    Provide      Review       ┌───┴───┐       │                  │
│   Issue +     Evidence     Both Sides   │       │       │                  │
│   Evidence                              ▼       ▼       ▼                  │
│                                     Full     Partial   No                   │
│                                    Refund   Refund   Refund                 │
│                                                                              │
│  TIMELINE: 7 days vendor response, 14 days admin resolution                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Step-by-Step

| Step | Actor | Action | Deadline | Data |
|------|-------|--------|----------|------|
| 1 | Buyer | Open dispute | After escalation or direct | `dispute_type` |
| 2 | Buyer | Describe issue | - | `description` |
| 3 | Buyer | Upload evidence | Photos, emails | `buyer_evidence[]` |
| 4 | Buyer | Submit | - | - |
| 5 | Vendor | Receive notification | - | - |
| 6 | Vendor | Respond within 7 days | Auto-lose if no response | - |
| 7 | Vendor | Provide evidence | Photos, tracking | `vendor_evidence[]` |
| 8 | Admin | Receive for review | - | - |
| 9 | Admin | Review all evidence | - | - |
| 10 | Admin | May request more info | Both parties | - |
| 11 | Admin | Make decision | Within 14 days | `decision` |
| 12 | System | Notify both parties | - | Email |
| 13 | System | Execute decision | Refund if applicable | - |
| 14 | System | Close dispute | - | `status: closed` |

---

# FLOW 9: SAAS TENANT LIFECYCLE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SAAS TENANT LIFECYCLE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │ SIGNUP │──▶│PROVISION│──▶│ TRIAL  │──▶│ACTIVATE│──▶│OPERATE │            │
│  │        │   │(Auto 5m)│   │(14 days)│  │(Pay)   │   │        │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│                                              │            │                 │
│                                              │            ▼                 │
│                                              │       ┌────────┐            │
│                                              │       │ MONTHLY│            │
│                                              │       │ BILLING│            │
│                                              │       └────────┘            │
│                                              │            │                 │
│                                              ▼            │                 │
│                                         ┌────────┐        │                 │
│                                         │NO PAY  │        │                 │
│                                         │SUSPEND │        │                 │
│                                         └────────┘        │                 │
│                                              │            │                 │
│                                              ▼            │                 │
│                                         ┌────────┐        │                 │
│                                         │CANCEL  │◀───────┘                 │
│                                         │(30 day)│  (On request)            │
│                                         └────────┘                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Provisioning (Automated)

| Step | Time | Action | Result |
|------|------|--------|--------|
| 1 | 0:00 | Signup form submitted | Request received |
| 2 | 0:05 | Validate slug unique | - |
| 3 | 0:10 | Create PostgreSQL database | tenant_slug_db |
| 4 | 0:30 | Initialize Odoo schema | Base tables |
| 5 | 1:00 | Install marketplace modules | Custom addon |
| 6 | 2:00 | Configure subdomain | tenant.somatech.ec |
| 7 | 3:00 | Provision SSL | Let's Encrypt |
| 8 | 4:00 | Create admin user | With temp password |
| 9 | 4:30 | Apply branding | Logo, colors |
| 10 | 5:00 | Send welcome email | Tenant ready! |

---

# FLOW 10: SRI INVOICE FLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SRI INVOICE FLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │ ORDER  │──▶│GENERATE│──▶│  SIGN  │──▶│  SEND  │──▶│RECEIVE │            │
│  │COMPLETE│   │  XML   │   │ XAdES  │   │ TO SRI │   │ AUTHOR │            │
│  └────────┘   └────────┘   └────────┘   └────────┘   └────────┘            │
│                   │            │            │            │                  │
│                   ▼            ▼            ▼            ▼                  │
│              XML 1.1.0    .p12 cert    SOAP call   Clave Acceso            │
│              Schema      SHA-256      Producción  49 digits                │
│                                                                              │
│                                                            │                │
│                                                            ▼                │
│                                                       ┌────────┐            │
│                                                       │GENERATE│            │
│                                                       │  RIDE  │            │
│                                                       └────────┘            │
│                                                            │                │
│                                                            ▼                │
│                                                       ┌────────┐            │
│                                                       │ EMAIL  │            │
│                                                       │TO BUYER│            │
│                                                       └────────┘            │
│                                                                              │
│  ERROR HANDLING:                                                            │
│  ├── SRI offline → Queue and retry every 5 min                              │
│  ├── Validation error → Log, alert admin                                    │
│  └── Signature error → Check certificate expiry                             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Step-by-Step

| Step | System | Action | Output |
|------|--------|--------|--------|
| 1 | Odoo | Order confirmed + paid | `sale.order.state = sale` |
| 2 | Odoo | Create invoice | `account.move` |
| 3 | l10n_ec_sri | Generate XML | Factura 1.1.0 schema |
| 4 | l10n_ec_sri | Generate claveAcceso | 49-digit key |
| 5 | l10n_ec_sri | Sign with XAdES | Using .p12 certificate |
| 6 | l10n_ec_sri | Send to SRI | SOAP: RecepcionComprobantesOffline |
| 7 | SRI | Validate | Return estado: RECIBIDA |
| 8 | l10n_ec_sri | Query authorization | SOAP: AutorizacionComprobantesOffline |
| 9 | SRI | Authorize | Return estado: AUTORIZADO |
| 10 | l10n_ec_sri | Store authorization | Save response XML |
| 11 | l10n_ec_sri | Generate RIDE | PDF with barcode |
| 12 | Odoo | Attach to invoice | Document link |
| 13 | Odoo | Email buyer | Invoice PDF + RIDE |

## Key Fields

| Field | Description | Example |
|-------|-------------|---------|
| `ruc_emisor` | Platform RUC | 1791234567001 |
| `razon_social` | Business name | SomaTech Ecuador S.A. |
| `fecha_emision` | Issue date | 24/01/2026 |
| `tipo_comprobante` | Invoice type | 01 (Factura) |
| `clave_acceso` | Access key | 49 digits |
| `numero_autorizacion` | SRI auth | Same as clave_acceso |

---

# SUMMARY: 10 CORE FLOWS

| # | Flow | Actors | Key Steps |
|---|------|--------|-----------|
| 1 | Vendor Lifecycle | Guest→Vendor, Admin | Register→Verify→Approve→Operate |
| 2 | Product Lifecycle | Vendor, Admin | Create→Submit→Review→Publish |
| 3 | B2C Purchase | Buyer, System | Browse→Cart→Checkout→Pay→Ship |
| 4 | B2B Purchase | B2B Buyer, Vendor | RFQ→Quote→Order→Net Terms→Pay |
| 5 | Order Fulfillment | Vendor, Carrier | Confirm→Pack→Ship→Deliver |
| 6 | Return/Refund | Buyer, Vendor, Admin | Request→Review→Ship Back→Refund |
| 7 | Commission/Payout | System, Vendor, Admin | Calculate→Hold→Release→Payout |
| 8 | Dispute | Buyer, Vendor, Admin | Open→Evidence→Review→Decision |
| 9 | SaaS Tenant | Operator, System | Signup→Provision→Trial→Activate |
| 10 | SRI Invoice | System, SRI | Generate→Sign→Send→Authorize→RIDE |

---

**END OF DOCUMENT**

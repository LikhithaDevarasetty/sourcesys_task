#  AI Analytics Dashboard

An interactive sales analytics dashboard built with **Streamlit** and **Plotly**, featuring a dark futuristic UI with your custom branding assets.

---

##  Preview

The dashboard uses a custom background, logo, and glassmorphism-style cards layered on a deep-space navy theme with a Plasma color palette across all charts.

---

##  Project Structure

```
project/
│
├── dashboard.py        # Main Streamlit application
├── requirements.txt    # Python dependencies
├── train.csv           # Sales dataset (Superstore format)
├── bg.png              # Background image
└── logo.png            # Brand logo
```

>  All four files — `train.csv`, `bg.png`, `logo.png`, and `dashboard.py` — must be in the **same folder** for the app to run correctly.

---


##  User Controls (Sidebar)

| Control | Description |
|---|---|
| **Year(s)** | Filter data by one or more order years (2015–2018) |
| **Region(s)** | Filter by geographic region (East, West, Central, South) |
| **Segment(s)** | Filter by customer segment (Consumer, Corporate, Home Office) |
| **Category(s)** | Filter by product category (Furniture, Office Supplies, Technology) |
| **X-Axis** | Choose what dimension drives the main chart |
| **Color By** | Choose the grouping variable for color encoding |
| **Chart Type** | Switch between Bar, Line, Area, Scatter, or Pie |

All filters apply globally across every chart on the page.

---

##  Charts Included

| Chart | Description |
|---|---|
| **Dynamic Main Chart** | Fully user-controlled via sidebar axis and chart type selectors |
| **Monthly Sales Trend** | Line chart comparing month-by-month sales across selected years |
| **Sales by Region** | Bar chart showing regional revenue breakdown |
| **Category Share** | Donut chart showing each category's revenue proportion |
| **Sub-Category Bar** | Horizontal bar ranked by sub-category sales |
| **Segment × Category** | Stacked bar showing how segments contribute per category |
| **Ship Mode Donut** | Shipping method distribution by revenue |
| **Quarterly Heatmap** | Year × Quarter grid showing seasonal patterns |
| **Top 10 States** | Bar chart of highest-revenue US states |

---

## 📦 Dataset Format

The app expects a CSV with the following columns:

```
Row ID, Order ID, Order Date, Ship Date, Ship Mode,
Customer ID, Customer Name, Segment, Country, City,
State, Postal Code, Region, Product ID, Category,
Sub-Category, Product Name, Sales
```

- **Order Date** and **Ship Date** should be in `DD/MM/YYYY` format.
- The **Sales** column must be numeric.



---

##  Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | 1.57.0 | Web app framework |
| `plotly` | 6.7.0 | Interactive charts |
| `pandas` | 3.0.2 | Data loading and transformation |

---


##  CSS Properties Used

All styling is injected via `st.markdown()` using a `<style>` block. Below is a breakdown of every CSS property used, grouped by the UI element it targets.

---

###  Global & Font

| Property | Value Used | Purpose |
|---|---|---|
| `@import` | Google Fonts — Inter | Loads the Inter typeface (weights 300–700) from Google's CDN |
| `font-family` | `'Inter', sans-serif` | Applied globally to all elements via `html, body, [class*="css"]` |

---

###  App Background (`.stApp`)

| Property | Value Used | Purpose |
|---|---|---|
| `background-image` | `url("data:image/png;base64,...")` | Embeds the `bg.png` background as a base64 inline image |
| `background-size` | `cover` | Scales the image to fill the entire viewport without gaps |
| `background-attachment` | `fixed` | Keeps the background pinned while content scrolls (parallax feel) |
| `background-position` | `center` | Centers the image in the viewport |

---

###  Dark Overlay (`.stApp::before`)

A pseudo-element placed over the background to darken it for readability.

| Property | Value Used | Purpose |
|---|---|---|
| `content` | `""` | Required to render a `::before` pseudo-element |
| `position` | `fixed` | Covers the full viewport regardless of scroll |
| `inset` | `0` | Shorthand for `top/right/bottom/left: 0` — fills the entire screen |
| `background` | `rgba(5, 8, 30, 0.72)` | Semi-transparent deep-navy layer dimming the background |
| `z-index` | `0` | Sits behind all UI content |
| `pointer-events` | `none` | Lets clicks pass through to elements underneath |

---

### Sidebar (`section[data-testid="stSidebar"] > div:first-child`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `rgba(10, 14, 50, 0.92)` | Deep navy with slight transparency |
| `border-right` | `1px solid rgba(100, 120, 255, 0.25)` | Subtle glowing right edge separating sidebar from content |
| `backdrop-filter` | `blur(18px)` | Blurs whatever is behind the sidebar panel (glassmorphism) |

---

###  Sidebar Labels (`.stSelectbox label`, `.stMultiSelect label`, `.stRadio label`)

| Property | Value Used | Purpose |
|---|---|---|
| `color` | `#a0b4ff` | Soft periwinkle blue for label text |
| `font-weight` | `500` | Medium weight for legibility |
| `font-size` | `0.82rem` | Slightly smaller than body text |
| `letter-spacing` | `0.05em` | Spreads characters for an uppercase label feel |
| `text-transform` | `uppercase` | Forces all label text to uppercase |

---

###  Sidebar Dropdowns (`div[data-baseweb="select"] > div`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `rgba(30, 40, 100, 0.7)` | Dark translucent blue input background |
| `border` | `1px solid rgba(100, 130, 255, 0.4)` | Faint blue border around the dropdown |
| `border-radius` | `10px` | Rounded corners on the select box |
| `color` | `#e0e8ff` | Light text color inside the dropdown |
| `border-color` *(focus)* | `#6c7fff` | Brighter border when the dropdown is active |
| `box-shadow` *(focus)* | `0 0 0 2px rgba(108, 127, 255, 0.35)` | Glowing ring effect on focus |

---

###  Metric Cards (`.metric-card`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `linear-gradient(135deg, rgba(20,28,90,0.85), rgba(40,20,100,0.75))` | Diagonal dark blue-to-purple gradient |
| `border` | `1px solid rgba(130, 100, 255, 0.35)` | Purple-tinted translucent border |
| `border-radius` | `16px` | Rounded card corners |
| `padding` | `22px 24px` | Inner spacing (vertical horizontal) |
| `backdrop-filter` | `blur(14px)` | Glassmorphism blur behind each card |
| `transition` | `transform 0.2s, box-shadow 0.2s` | Smooth animation on hover |
| `text-align` | `center` | Centers all card content |
| `transform` *(hover)* | `translateY(-4px)` | Card lifts upward on mouse hover |
| `box-shadow` *(hover)* | `0 12px 40px rgba(100, 80, 255, 0.3)` | Purple glow shadow on hover |

---

### Metric Card Text

| Selector | Property | Value | Purpose |
|---|---|---|---|
| `.metric-label` | `color` | `#8899dd` | Muted blue-grey for the label line |
| `.metric-label` | `font-size` | `0.75rem` | Small uppercase caption |
| `.metric-label` | `font-weight` | `600` | Semi-bold |
| `.metric-label` | `letter-spacing` | `0.1em` | Spread letters for caps label style |
| `.metric-label` | `text-transform` | `uppercase` | All caps label |
| `.metric-label` | `margin-bottom` | `6px` | Space between label and value |
| `.metric-value` | `color` | `#ffffff` | Bright white for the main number |
| `.metric-value` | `font-size` | `1.9rem` | Large display number |
| `.metric-value` | `font-weight` | `700` | Bold |
| `.metric-value` | `line-height` | `1.1` | Tighter line height for large text |
| `.metric-delta` | `color` | `#66ffb2` | Mint green for the delta/subtitle line |
| `.metric-delta` | `font-size` | `0.78rem` | Smallest text in the card |
| `.metric-delta` | `margin-top` | `5px` | Space above delta text |

---

###  Chart Wrapper (`.chart-box`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `rgba(10, 15, 55, 0.75)` | Semi-transparent dark navy panel |
| `border` | `1px solid rgba(90, 110, 255, 0.25)` | Subtle blue border around each chart |
| `border-radius` | `18px` | Rounded container edges |
| `padding` | `20px` | Inner breathing room around the chart |
| `backdrop-filter` | `blur(16px)` | Glassmorphism blur effect |
| `margin-bottom` | `20px` | Vertical gap between chart boxes |

---

###  Chart Title (`.chart-title`)

| Property | Value Used | Purpose |
|---|---|---|
| `color` | `#c0caff` | Soft lavender-blue text |
| `font-size` | `0.9rem` | Slightly smaller than body text |
| `font-weight` | `600` | Semi-bold |
| `letter-spacing` | `0.08em` | Spaced for an uppercase label feel |
| `text-transform` | `uppercase` | All-caps section label |
| `margin-bottom` | `12px` | Space below the title |
| `padding-bottom` | `10px` | Space before the divider line |
| `border-bottom` | `1px solid rgba(100, 120, 255, 0.2)` | Thin separator line under the title |

---

###  Logo Bar (`.logo-bar`, `.logo-bar img`, `.logo-bar-text`)

| Property | Value Used | Purpose |
|---|---|---|
| `display` | `flex` | Enables flexbox layout for horizontal alignment |
| `align-items` | `center` | Vertically centers the logo and text |
| `gap` | `14px` | Space between logo image and text |
| `padding` | `10px 0 18px` | Top and bottom spacing |
| `width` *(img)* | `90px` | Fixed logo image width |
| `border-radius` *(img)* | `12px` | Rounded logo corners |
| `font-size` *(text)* | `1.05rem` | Brand name font size |
| `font-weight` *(text)* | `700` | Bold brand text |
| `color` *(text)* | `#a8baff` | Periwinkle brand color |
| `letter-spacing` *(text)* | `0.06em` | Slightly spaced for branding feel |
| `line-height` *(text)* | `1.35` | Controls spacing between the two text lines |

---

###  Sidebar Divider (`.sidebar-divider`)

| Property | Value Used | Purpose |
|---|---|---|
| `border` | `none` | Removes default `<hr>` border |
| `border-top` | `1px solid rgba(100, 130, 255, 0.2)` | Custom thin translucent blue line |
| `margin` | `14px 0` | Vertical spacing above and below the divider |

---

### Streamlit UI Cleanup

| Selector | Property | Value | Purpose |
|---|---|---|---|
| `footer` | `visibility` | `hidden` | Hides Streamlit's default footer |
| `#MainMenu` | `visibility` | `hidden` | Hides the hamburger menu |
| `.stPlotlyChart` | `border-radius` | `14px` | Rounds the Plotly chart iframe corners |
| `div[data-testid="stHorizontalBlock"]` | `gap` | `16px` | Adds spacing between side-by-side columns |

---

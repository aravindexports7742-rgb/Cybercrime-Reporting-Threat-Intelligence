# Migrate Dashboard to Modern Next.js (React)

You want to move away from Streamlit and run a native, modern React dashboard! This is a great choice as it will provide a much smoother user experience, better aesthetics, and a cohesive feel with your existing landing page.

I will use the `dashboard-mockup.html` file you already have in the project root as the design foundation, converting it into reusable React components using Tailwind CSS.

## User Review Required

> [!IMPORTANT]
> **Streamlit Deprecation**
> This change will effectively deprecate the `frontend_streamlit` application. All frontend functionality will now live inside the `frontend` folder (Next.js). The FastAPI backend (`backend/main.py`) will remain untouched and serve as the API for this new Next.js dashboard. 
>
> If this sounds good to you, please click **Proceed**.

## Open Questions

> [!WARNING]
> Do you have any specific preferences for state management (e.g., React Context vs. Zustand) for handling user authentication? If not, I will use a simple React Context provider to manage the logged-in user and role.

## Proposed Changes

We will build out the following architecture in your Next.js application:

### Authentication & Routing
- Update Next.js config/middleware or use React Context to protect `/dashboard` routes.
- **[NEW]** `src/context/AuthContext.tsx`: To store the JWT token and current user role.
- **[NEW]** `src/app/login/page.tsx`: A beautiful login page that hits the FastAPI `/auth/login` endpoint and redirects to the appropriate dashboard.

### Dashboard Core Components (Based on Mockup)
- **[NEW]** `src/app/dashboard/layout.tsx`: A shared layout containing the sidebar and top navigation bar.
- **[NEW]** `src/components/dashboard/Sidebar.tsx`: The left navigation menu from your mockup.
- **[NEW]** `src/components/dashboard/Topbar.tsx`: The top bar with breadcrumbs and user profile.
- **[NEW]** `src/components/dashboard/KpiCard.tsx`: Reusable KPI card components.

### Role-Based Pages
We will create placeholder pages for each sector that you can later expand with full API integration:
- **[NEW]** `src/app/dashboard/victim/page.tsx`: The Victim Portal Dashboard.
- **[NEW]** `src/app/dashboard/officer/page.tsx`: The Officer Portal Dashboard.
- **[NEW]** `src/app/dashboard/threat/page.tsx`: Threat Intelligence Dashboard.
- **[NEW]** `src/app/dashboard/admin/page.tsx`: Incident Response & Admin Dashboard.

### Integration
- **[MODIFY]** `src/app/page.tsx`: Revert the links back to `/login` so the landing page connects to our new Next.js login page.

## Verification Plan

### Manual Verification
1. Open the landing page and click "Enter Dashboard".
2. You will be routed to the new Next.js `/login` page.
3. Authenticate with a test user via the FastAPI backend.
4. Verify you are redirected to the modern React dashboard layout corresponding to your role, matching the design of `dashboard-mockup.html`.

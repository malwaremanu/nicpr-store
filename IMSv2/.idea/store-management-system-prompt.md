# Store Management System Implementation Guide

## System Overview

Create a Flask-based store management system for handling requisition requests, approval workflows, inventory tracking, and procurement. The system needs to support multiple user roles with different permissions in a hierarchical approval process.

## Core Requirements

1. **User Roles & Hierarchy:**
   - Simple Users: Initiate requisition requests
   - Division Heads: First-level approval
   - Store Incharge: Second-level approval
   - Store Assistant: Fulfills requests and manages inventory
   - Admin: Manages store and inventory
   - Superadmin: Complete system access

2. **Requisition Workflow:**
   - User raises a request for required items
   - Division Head approves/rejects
   - Store Incharge reviews approved requests
   - Store Assistant fulfills from inventory
   - Notifications at each stage

3. **Inventory Management:**
   - Track current stock levels
   - Minimum stock threshold alerts
   - Location tracking within store

4. **Item Substitution:**
   - Users may request generic items (e.g., "mouse")
   - Store Assistant selects specific available items

5. **Partial Fulfillment:**
   - Allow partial fulfillment when stock is limited
   - Automatic purchase request generation for unavailable items

## Data Structure

Design a simple JSON-based data storage system as follows:

1. **Users:** ID, username, password, role, division_id
2. **Divisions:** ID, name, head_id
3. **Items:** ID, name, description, category, minimum_stock, unit_price
4. **Inventory:** ID, item_id, quantity, location
5. **Requests:** ID, requester_id, division_id, date, status, items array, remarks, current_approver

## Core Features

1. **Authentication & Authorization:**
   - Role-based access control
   - Session management
   - Permission checks for each workflow stage

2. **Request Management:**
   - Create new requests with multiple items
   - Track request status through approval chain
   - Filter requests by role and division

3. **Inventory Operations:**
   - Stock updates when fulfilling requests
   - Low stock alerts based on minimum thresholds
   - Stock history tracking

4. **Admin Functions:**
   - Item and category management
   - User management
   - System dashboard with key metrics

## Implementation Details

1. **File Structure:**
   - Follow MVC-like pattern with routes, templates, and data models
   - Centralize data loading/saving functions
   - Create reusable decorators for auth checks

2. **Database Approach:**
   - Use JSON files for simplicity
   - Create default data if files don't exist
   - Implement functions to save data after modifications

3. **Template Organization:**
   - Base template with navigation
   - Section-specific templates (admin, inventory, requests)
   - Form templates for various operations

4. **Workflow Implementation:**
   - Use a "current_approver" field to track workflow stage
   - Status updates at each approval/rejection step
   - Role-based filtering of request lists

5. **Minimal Interface Focus:**
   - Clean, functional UI without complex styling
   - Form-based interactions
   - Clear status indicators

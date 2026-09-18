import { Link, useLocation, useNavigate } from 'react-router-dom'
import {
    LayoutDashboard,
    Search,
    PlusCircle,
    Banknote,
    ArrowLeftRight,
    LogOut,
} from 'lucide-react'
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from '@/components/ui/sidebar'
import { clearCurrentUser } from '@/currentUser'

const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/lookup', label: 'Transaction Lookup', icon: Search },
    { to: '/accounts/new', label: 'Create New Account', icon: PlusCircle },
    { to: '/withdraw', label: 'Withdraw', icon: Banknote },
    { to: '/deposit', label: 'Deposit', icon: Banknote },
    { to: '/transfer', label: 'Transfer', icon: ArrowLeftRight },
]

function AppSidebar() {
    const location = useLocation()
    const navigate = useNavigate()

    /* Drop the stored user and land back on the public homepage */
    function handleSignOut() {
        clearCurrentUser()
        navigate('/', { replace: true })
    }

    return (
        <Sidebar collapsible="icon">
            <SidebarHeader className="px-4 py-3 text-lg font-semibold">
                Best Banking App
            </SidebarHeader>

            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {navItems.map(({ to, label, icon: Icon }) => (
                                <SidebarMenuItem key={to}>
                                    <SidebarMenuButton
                                        asChild
                                        isActive={location.pathname === to}
                                        tooltip={label}
                                    >
                                        <Link to={to}>
                                            <Icon />
                                            <span>{label}</span>
                                        </Link>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>

            <SidebarFooter>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton onClick={handleSignOut} tooltip="Sign out">
                            <LogOut />
                            <span>Sign out</span>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarFooter>
        </Sidebar>
    )
}

export default AppSidebar

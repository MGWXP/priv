// Dashboard preview component for the priv system.

import React, { useState } from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, ResponsiveContainer,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell
} from 'recharts';
import {
  Server, Database, GitBranch, Code, AlertCircle, Check,
  Cpu, Activity, Zap, Globe, Command, RefreshCw
} from 'lucide-react';

// Mock data
const systemMetrics = {
  uptime: 259200, // 3 days in seconds
  memoryUsage: 2.4, // GB
  cpuUsage: 28, // percentage
  activeProcesses: 6,
  schemaCount: 12,
  successRate: 0.98, // 98%
};

const serviceStatus = [
  { name: 'socket-server', status: 'online', uptime: 259200, memoryUsage: 512, cpu: 12.3 },
  { name: 'schema-registry', status: 'online', uptime: 259200, memoryUsage: 345, cpu: 8.7 },
  { name: 'streaming-transformer', status: 'online', uptime: 259200, memoryUsage: 487, cpu: 14.2 },
  { name: 'notion-connection', status: 'online', uptime: 259200, memoryUsage: 623, cpu: 15.8 },
  { name: 'mcp-orchestrator', status: 'online', uptime: 259200, memoryUsage: 389, cpu: 9.4 },
];

const performanceHistory = [
  { time: '00:00', cpu: 25, memory: 2.1, requests: 15 },
  { time: '01:00', cpu: 28, memory: 2.2, requests: 16 },
  { time: '02:00', cpu: 32, memory: 2.3, requests: 18 },
  { time: '03:00', cpu: 35, memory: 2.4, requests: 17 },
  { time: '04:00', cpu: 30, memory: 2.4, requests: 19 },
  { time: '05:00', cpu: 28, memory: 2.3, requests: 20 },
  { time: '06:00', cpu: 25, memory: 2.2, requests: 18 },
  { time: '07:00', cpu: 22, memory: 2.1, requests: 17 },
  { time: '08:00', cpu: 26, memory: 2.2, requests: 16 },
  { time: '09:00', cpu: 28, memory: 2.3, requests: 18 },
  { time: '10:00', cpu: 30, memory: 2.4, requests: 19 },
  { time: '11:00', cpu: 32, memory: 2.5, requests: 20 },
];

const errorDistribution = [
  { name: 'Socket Connection', value: 15, color: '#ef4444' },
  { name: 'Schema Validation', value: 8, color: '#f59e0b' },
  { name: 'Notion API', value: 12, color: '#3b82f6' },
  { name: 'Process Management', value: 5, color: '#a855f7' },
  { name: 'Memory Issues', value: 3, color: '#ec4899' },
];

const notionStats = {
  connectedWorkspaces: 2,
  activeDatabases: 12,
  activeBlocks: 87,
};

const githubStats = {
  connectedRepositories: 5,
  totalBranches: 12,
  pullRequests: { open: 3, merged: 8, closed: 2 },
};

// Theme configuration
const THEME = {
  primary: '#6366f1',
  secondary: '#22c55e',
  tertiary: '#f59e0b',
  quaternary: '#ef4444',
  info: '#3b82f6',
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  background: '#f8fafc',
  card: '#ffffff',
  text: {
    primary: '#1e293b',
    secondary: '#64748b',
    faded: '#94a3b8'
  },
  border: '#e2e8f0',
  accent: {
    purple: '#a855f7',
    blue: '#3b82f6',
    green: '#10b981',
    yellow: '#f59e0b',
    red: '#ef4444',
    pink: '#ec4899',
    indigo: '#6366f1'
  }
};

// Helper functions
const formatUptime = (seconds) => {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (days > 0) {
    return `${days}d ${hours}h ${minutes}m`;
  } else if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else {
    return `${minutes}m`;
  }
};

// Component definitions
const StatusBadge = ({ status }) => {
  const colors = {
    online: THEME.success,
    error: THEME.error,
    warning: THEME.warning,
    offline: THEME.error
  };
  
  return (
    <div className="flex items-center">
      <div 
        className="w-2.5 h-2.5 rounded-full mr-2" 
        style={{ backgroundColor: colors[status] }}
      />
      <span className="capitalize">{status}</span>
    </div>
  );
};

const MetricsCard = ({ title, value, icon, color, subtitle = null, trend = null }) => {
  return (
    <div className="bg-white rounded-lg shadow p-5 transition duration-300 hover:shadow-lg">
      <div className="flex justify-between items-center mb-3">
        <div className="p-3 rounded-lg" style={{ backgroundColor: `${color}16` }}>
          {React.cloneElement(icon, { color: color, size: 22 })}
        </div>
        {trend !== null && (
          <div className="flex items-center" style={{ color: trend > 0 ? THEME.success : THEME.error }}>
            {trend > 0 ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0L10 7.586l2.293-2.293a1 1 0 011.414 0l3 3a1 1 0 010 1.414 1 1 0 01-1.414 0L13 7.414l-2.293 2.293a1 1 0 01-1.414 0L7 7.414l-2.293 2.293a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M16.707 10.293a1 1 0 010 1.414l-3 3a1 1 0 01-1.414 0L10 12.414l-2.293 2.293a1 1 0 01-1.414 0l-3-3a1 1 0 111.414-1.414L7 12.586l2.293-2.293a1 1 0 011.414 0L13 12.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            )}
            <span className="text-sm font-medium">{Math.abs(trend)}%</span>
          </div>
        )}
      </div>
      <div>
        <h3 className="text-gray-500 text-sm mb-1">{title}</h3>
        <p className="text-2xl font-bold">{value}</p>
        {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
      </div>
    </div>
  );
};

const ServiceListItem = ({ service, expanded = false }) => {
  return (
    <div 
      className="bg-white rounded-lg shadow mb-3 overflow-hidden transition-all duration-300"
      style={{ borderLeft: `4px solid ${service.status === 'online' ? THEME.success : THEME.error}` }}
    >
      <div className="p-4 flex justify-between items-center">
        <div className="flex items-center">
          <Server size={18} className="mr-3 text-gray-500" />
          <span className="font-medium">{service.name}</span>
        </div>
        <div className="flex items-center space-x-4">
          <StatusBadge status={service.status} />
          <span className="text-sm text-gray-500">{formatUptime(service.uptime)}</span>
          <div className="text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatusCard = ({ title, children, icon, className = '', footer = null }) => {
  return (
    <div className={`bg-white rounded-lg shadow overflow-hidden ${className}`}>
      <div className="p-4 border-b border-gray-100 flex items-center">
        {React.cloneElement(icon, { size: 18, className: 'mr-2 text-indigo-600' })}
        <h3 className="font-semibold text-gray-800">{title}</h3>
      </div>
      <div className="p-4">
        {children}
      </div>
      {footer && (
        <div className="px-4 py-3 bg-gray-50 border-t border-gray-100">
          {footer}
        </div>
      )}
    </div>
  );
};

const privDashboardPreview = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [viewMode, setViewMode] = useState('visual');
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <header className="mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 gap-y-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">priv System Dashboard</h1>
              <p className="text-gray-600">Codex-Notion Integration Framework</p>
            </div>
            <div className="flex space-x-4">
              <div className="flex bg-white shadow rounded-lg px-4 py-2 items-center">
                <Cpu className="text-indigo-600 mr-2" size={20} />
                <span className="font-medium text-gray-700">M3 Max Optimized</span>
              </div>
              <div className="flex bg-white shadow rounded-lg px-4 py-2 items-center">
                <Activity className="text-green-600 mr-2" size={20} />
                <span className="font-medium text-gray-700">Uptime: {formatUptime(systemMetrics.uptime)}</span>
              </div>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
            <nav className="mb-4 sm:mb-0 border-b border-gray-200 w-full sm:w-auto">
              <ul className="flex space-x-4 sm:space-x-8">
                <li>
                  <button 
                    className={`py-2 px-1 ${activeTab === 'overview' ? 'border-b-2 border-indigo-600 text-indigo-600 font-medium' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('overview')}
                  >
                    Overview
                  </button>
                </li>
                <li>
                  <button 
                    className={`py-2 px-1 ${activeTab === 'services' ? 'border-b-2 border-indigo-600 text-indigo-600 font-medium' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('services')}
                  >
                    Services
                  </button>
                </li>
                <li>
                  <button 
                    className={`py-2 px-1 ${activeTab === 'architecture' ? 'border-b-2 border-indigo-600 text-indigo-600 font-medium' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('architecture')}
                  >
                    Architecture
                  </button>
                </li>
                <li>
                  <button 
                    className={`py-2 px-1 ${activeTab === 'github' ? 'border-b-2 border-indigo-600 text-indigo-600 font-medium' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('github')}
                  >
                    GitHub
                  </button>
                </li>
                <li>
                  <button 
                    className={`py-2 px-1 ${activeTab === 'notion' ? 'border-b-2 border-indigo-600 text-indigo-600 font-medium' : 'text-gray-500'}`}
                    onClick={() => setActiveTab('notion')}
                  >
                    Notion
                  </button>
                </li>
              </ul>
            </nav>
            
            <div className="flex items-center space-x-2 bg-white shadow rounded-lg px-3 py-2">
              <button 
                className={`px-3 py-1 rounded-md text-sm ${viewMode === 'visual' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700'}`}
                onClick={() => setViewMode('visual')}
              >
                Visual
              </button>
              <button 
                className={`px-3 py-1 rounded-md text-sm ${viewMode === 'data' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700'}`}
                onClick={() => setViewMode('data')}
              >
                Data
              </button>
            </div>
          </div>
        </header>
        
        {/* Overview Tab Content */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricsCard 
                title="CPU Usage" 
                value={`${systemMetrics.cpuUsage}%`} 
                icon={<Cpu />} 
                color={THEME.accent.blue}
                trend={-2.4}
              />
              <MetricsCard
                title="Memory Usage"
                value={`${systemMetrics.memoryUsage.toFixed(1)} GB`}
                icon={<Cpu />}
                color={THEME.accent.green}
                trend={1.2}
              />

              <MetricsCard 
                title="Active Services" 
                value={systemMetrics.activeProcesses} 
                icon={<Server />} 
                color={THEME.accent.purple}
              />
              <MetricsCard 
                title="Schema Count" 
                value={systemMetrics.schemaCount} 
                icon={<Database />} 
                color={THEME.accent.yellow}
                trend={8.3}
              />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <StatusCard title="System Status" icon={<Activity />}>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={serviceStatus.map(s => ({ name: s.name, memory: s.memoryUsage, cpu: s.cpu }))}
                      margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis yAxisId="left" orientation="left" stroke={THEME.accent.blue} />
                      <YAxis yAxisId="right" orientation="right" stroke={THEME.accent.green} />
                      <Tooltip />
                      <Legend />
                      <Bar yAxisId="left" dataKey="cpu" name="CPU %" fill={THEME.accent.blue} />
                      <Bar yAxisId="right" dataKey="memory" name="Memory (MB)" fill={THEME.accent.green} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </StatusCard>
              
              <StatusCard title="Performance Metrics" icon={<Activity />}>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                      data={performanceHistory}
                      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis yAxisId="left" />
                      <YAxis yAxisId="right" orientation="right" />
                      <Tooltip />
                      <Legend />
                      <Line yAxisId="left" type="monotone" dataKey="cpu" stroke={THEME.accent.blue} name="CPU (%)" activeDot={{ r: 8 }} />
                      <Line yAxisId="left" type="monotone" dataKey="memory" stroke={THEME.accent.green} name="Memory (GB)" />
                      <Line yAxisId="right" type="monotone" dataKey="requests" stroke={THEME.accent.purple} name="Requests/s" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </StatusCard>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <StatusCard title="MCP Server Status" icon={<Globe />}>
                <div className="space-y-3">
                  {['filesystem', 'notion', 'slack', 'github'].map((server) => (
                    <div key={server} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                      <div className="flex items-center">
                        <div className="w-8 h-8 rounded-md flex items-center justify-center mr-3 bg-green-100">
                          <Server size={18} color={THEME.accent.green} />
                        </div>
                        <div>
                          <p className="font-medium text-gray-800">{server}</p>
                          <p className="text-xs text-gray-500">PID: {12350 + Math.floor(Math.random() * 10)}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <StatusBadge status="online" />
                        <button className="p-1 rounded-md hover:bg-gray-100">
                          <RefreshCw size={16} className="text-gray-500" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </StatusCard>
              
              <StatusCard title="Error Distribution" icon={<AlertCircle />}>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={errorDistribution}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        fill="#8884d8"
                        paddingAngle={5}
                        dataKey="value"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {errorDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`${value} errors`, 'Count']} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </StatusCard>
            </div>
            
            <StatusCard title="Command Terminal" icon={<Command />}>
              <div className="w-full rounded-lg overflow-hidden shadow-lg bg-gray-800 text-white">
                {/* Terminal Header */}
                <div className="bg-gray-700 px-4 py-2 flex justify-between items-center">
                  <div className="flex space-x-2 items-center">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  </div>
                  <div className="font-mono text-xs text-gray-300">Command Terminal</div>
                  <div className="w-4"></div> {/* Spacer for balance */}
                </div>
                
                {/* Terminal Content */}
                <div className="p-4 font-mono text-sm h-40 overflow-y-auto">
                  <div className="flex flex-col space-y-2">
                    <div className="leading-relaxed">
                      <div className="flex">
                        <span className="text-green-400">user@priv-system</span>
                        <span className="text-white mx-1">:</span>
                        <span className="text-blue-400">~/Desktop/anchor-core</span>
                        <span className="text-white mx-1">$</span>
                      </div>
                      <div className="ml-4 text-white">./priv status</div>
                      <div className="ml-4 text-gray-300 mt-1">
                        <div className="leading-relaxed">✅ All services are running</div>
                        <div className="leading-relaxed">System Resources</div>
                        <div className="leading-relaxed">════════════════════════════════════════</div>
                        <div className="leading-relaxed">CPU Usage: 28.4%</div>
                        <div className="leading-relaxed">Memory Usage: 2.4GB</div>
                      </div>
                    </div>
                    
                    {/* Blinking cursor */}
                    <div className="flex items-center">
                      <span className="text-green-400">user@priv-system</span>
                      <span className="text-white mx-1">:</span>
                      <span className="text-blue-400">~/Desktop/anchor-core</span>
                      <span className="text-white mx-1">$</span>
                      <span className="w-3 h-5 bg-gray-300 animate-pulse"></span>
                    </div>
                  </div>
                </div>
              </div>
            </StatusCard>
          </div>
        )}
        
        {/* Services Tab */}
        {activeTab === 'services' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-2">
                <StatusCard title="Service Status" icon={<Server />} className="h-full">
                  <div className="space-y-0">
                    {serviceStatus.map((service) => (
                      <ServiceListItem 
                        key={service.name} 
                        service={service}
                      />
                    ))}
                    
                    <div className="pt-4 border-t border-gray-100 mt-6">
                      <h4 className="font-medium text-gray-800 mb-3">MCP Servers</h4>
                      {['filesystem', 'notion', 'slack', 'github'].map((serverName) => (
                        <ServiceListItem 
                          key={serverName} 
                          service={{ 
                            name: serverName, 
                            status: 'online', 
                            uptime: 259200, 
                            memoryUsage: 412, 
                            cpu: 11.2
                          }}
                        />
                      ))}
                    </div>
                  </div>
                </StatusCard>
              </div>
              
              <div className="space-y-6">
                <StatusCard title="Resource Allocation" icon={<Cpu />}>
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-2">CPU Allocation</h4>
                    <div className="h-32">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={serviceStatus.slice(0, 3)}
                          margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                          layout="vertical"
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis type="number" domain={[0, 25]} />
                          <YAxis type="category" dataKey="name" width={120} />
                          <Tooltip />
                          <Bar dataKey="cpu" fill={THEME.accent.blue} name="CPU %" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </StatusCard>
                
                <StatusCard title="System Performance" icon={<Activity />}>
                  <div className="space-y-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-1">CPU Usage</h4>
                      <div className="flex items-center">
                        <div className="w-full h-2 bg-gray-200 rounded-full mr-2">
                          <div 
                            className="h-full rounded-full"
                            style={{ width: `${systemMetrics.cpuUsage}%`, backgroundColor: THEME.accent.blue }} 
                          ></div>
                        </div>
                        <span className="text-xs font-medium">{systemMetrics.cpuUsage}%</span>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-1">Memory Usage</h4>
                      <div className="flex items-center">
                        <div className="w-full h-2 bg-gray-200 rounded-full mr-2">
                          <div 
                            className="h-full rounded-full" 
                            style={{ width: `${systemMetrics.memoryUsage * 10}%`, backgroundColor: THEME.accent.green }}
                          ></div>
                        </div>
                        <span className="text-xs font-medium">{systemMetrics.memoryUsage.toFixed(1)} GB</span>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-1">Success Rate</h4>
                      <div className="flex items-center">
                        <div className="w-full h-2 bg-gray-200 rounded-full mr-2">
                          <div 
                            className="h-full rounded-full" 
                            style={{ width: `${systemMetrics.successRate * 100}%`, backgroundColor: THEME.accent.blue }}
                          ></div>
                        </div>
                        <span className="text-xs font-medium">{(systemMetrics.successRate * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                </StatusCard>
              </div>
            </div>
          </div>
        )}
        
        {/* Architecture Tab */}
        {activeTab === 'architecture' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <StatusCard title="System Architecture" icon={<Server />}>
              <div className="bg-white p-4 rounded-lg shadow-inner">
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 h-64 flex items-center justify-center">
                  <svg width="100%" height="100%" viewBox="0 0 800 500">
                    {/* Simplified connection diagram */}
                    {/* Connections */}
                    <path d="M 400 80 L 400 180" stroke="#6366f1" strokeWidth="2" />
                    <path d="M 400 180 L 200 270" stroke="#6366f1" strokeWidth="2" />
                    <path d="M 400 180 L 580 270" stroke="#6366f1" strokeWidth="2" />
                    <path d="M 200 270 L 400 340" stroke="#6366f1" strokeWidth="2" />
                    <path d="M 580 270 L 400 340" stroke="#6366f1" strokeWidth="2" />
                    <path d="M 400 340 L 320 430" stroke="#6366f1" strokeWidth="2" />
                    <path d="M 400 340 L 480 430" stroke="#6366f1" strokeWidth="2" />
                    
                    {/* Nodes */}
                    {/* Codex */}
                    <circle cx="400" cy="80" r="30" fill="white" stroke="#3b82f6" strokeWidth="2" />
                    <text x="400" y="85" textAnchor="middle" fontSize="22" fill="#3b82f6">👤</text>
                    <text x="400" y="135" textAnchor="middle" fontSize="12" fill="#1e293b">Codex</text>
                    
                    {/* Socket Server */}
                    <circle cx="400" cy="180" r="30" fill="white" stroke="#10b981" strokeWidth="2" />
                    <text x="400" y="185" textAnchor="middle" fontSize="22" fill="#10b981">🖥️</text>
                    <text x="400" y="235" textAnchor="middle" fontSize="12" fill="#1e293b">Socket Server</text>
                    
                    {/* Schema Registry */}
                    <circle cx="200" cy="270" r="30" fill="white" stroke="#10b981" strokeWidth="2" />
                    <text x="200" y="275" textAnchor="middle" fontSize="22" fill="#10b981">🖥️</text>
                    <text x="200" y="325" textAnchor="middle" fontSize="12" fill="#1e293b">Schema Registry</text>
                    
                    {/* MCP Orchestrator */}
                    <circle cx="580" cy="270" r="30" fill="white" stroke="#10b981" strokeWidth="2" />
                    <text x="580" y="275" textAnchor="middle" fontSize="22" fill="#10b981">🖥️</text>
                    <text x="580" y="325" textAnchor="middle" fontSize="12" fill="#1e293b">MCP Orchestrator</text>
                    
                    {/* Streaming Transformer */}
                    <circle cx="400" cy="340" r="30" fill="white" stroke="#10b981" strokeWidth="2" />
                    <text x="400" y="345" textAnchor="middle" fontSize="22" fill="#10b981">🖥️</text>
                    <text x="400" y="395" textAnchor="middle" fontSize="12" fill="#1e293b">Streaming Transformer</text>
                    
                    {/* Notion Connection */}
                    <circle cx="320" cy="430" r="30" fill="white" stroke="#f59e0b" strokeWidth="2" />
                    <text x="320" y="435" textAnchor="middle" fontSize="22" fill="#f59e0b">🔌</text>
                    <text x="320" y="485" textAnchor="middle" fontSize="12" fill="#1e293b">Notion Connection</text>
                    
                    {/* GitHub Connection */}
                    <circle cx="480" cy="430" r="30" fill="white" stroke="#f59e0b" strokeWidth="2" />
                    <text x="480" y="435" textAnchor="middle" fontSize="22" fill="#f59e0b">🔌</text>
                    <text x="480" y="485" textAnchor="middle" fontSize="12" fill="#1e293b">GitHub Connection</text>
                  </svg>
                </div>
              </div>
            </StatusCard>
            
            <div className="bg-white rounded-lg shadow p-4">
              <div className="mb-4 border-b pb-2">
                <h3 className="font-semibold text-gray-800">Module System Architecture</h3>
              </div>
              
              <div className="flex flex-col space-y-4">
                {/* Package.json */}
                <div className="flex items-start rounded-md bg-gray-50 p-3">
                  <div className="w-16 h-16 flex-shrink-0 flex items-center justify-center bg-indigo-100 text-indigo-600 rounded-md">
                    <Code size={32} />
                  </div>
                  <div className="ml-4 flex-1">
                    <h4 className="font-medium text-gray-800">package.json</h4>
                    <p className="text-sm text-gray-600 mb-1">Type: <span className="font-medium">commonjs</span></p>
                    <div className="bg-gray-700 rounded p-2 overflow-x-auto mt-2 text-left">
                      <pre className="text-xs text-gray-200">
{`{
  "name": "priv",
  "version": "1.5.0",
  "type": "commonjs",
  "description": "Codex-Notion Integration Framework"
}`}
                      </pre>
                    </div>
                    </div>
                  </div>
                </div>
                
                {/* Core Directory */}
                <div className="flex items-start rounded-md bg-gray-50 p-3">
                  <div className="w-16 h-16 flex-shrink-0 flex items-center justify-center bg-green-100 text-green-600 rounded-md">
                    <Server size={32} />
                  </div>
                  <div className="ml-4 flex-1">
                    <h4 className="font-medium text-gray-800">Core Implementation</h4>
                    <p className="text-sm text-gray-600 mb-1">File Extension: <span className="font-medium">.cjs</span></p>
                    <div className="flex flex-wrap gap-2 mt-2">
                      <div className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">socket-server.cjs</div>
                      <div className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">schema-registry.cjs</div>
                      <div className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">streaming-transformer.cjs</div>
                      <div className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">notion-connection-manager.cjs</div>
                      <div className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">mcp-orchestrator.cjs</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* GitHub Tab */}
        {activeTab === 'github' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <MetricsCard 
                title="Connected Repositories" 
                value={githubStats.connectedRepositories} 
                icon={<Database />} 
                color={THEME.accent.blue}
              />
              <MetricsCard 
                title="Total Branches" 
                value={githubStats.totalBranches} 
                icon={<GitBranch />} 
                color={THEME.accent.green}
              />
              <MetricsCard 
                title="Open Pull Requests" 
                value={githubStats.pullRequests.open} 
                icon={<Code />} 
                color={THEME.accent.purple}
                subtitle={`${githubStats.pullRequests.merged} merged, ${githubStats.pullRequests.closed} closed`}
              />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <StatusCard title="Git Status" icon={<GitBranch />}>
                <div className="space-y-4">
                  <div className="flex justify-between items-center border-b border-gray-100 pb-3">
                    <div>
                      <span className="text-gray-500 text-sm">Current Branch</span>
                      <div className="flex items-center mt-1">
                        <GitBranch size={16} className="text-indigo-600 mr-2" />
                        <span className="font-medium">main</span>
                      </div>
                    </div>
                    <div className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">
                      8 uncommitted changes
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-gray-500 text-sm">Last Commit</span>
                    <div className="flex items-center mt-1">
                      <span className="font-medium">May 19, 3:30 PM</span>
                    </div>
                    <p className="text-gray-700 mt-1">Fix schema registry module system compatibility</p>
                  </div>
                  
                  <div>
                    <h4 className="text-gray-500 text-sm mb-2">Modified Files</h4>
                    <div className="space-y-2">
                      {['core/schema-registry.cjs', 'entry-points/schema-registry-main.js', 'launch-optimized.sh'].map(file => (
                        <div key={file} className="flex items-center bg-gray-50 px-3 py-2 rounded-md">
                          <div className="w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                          <span className="text-sm font-mono">{file}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </StatusCard>
              
              <StatusCard title="Contributors" icon={<Server />}>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'XPV', commits: 67, color: THEME.accent.blue },
                          { name: 'Nexa', commits: 42, color: THEME.accent.green },
                          { name: 'Axiomatic', commits: 23, color: THEME.accent.purple },
                          { name: 'MCP', commits: 15, color: THEME.accent.yellow },
                        ]}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        fill="#8884d8"
                        paddingAngle={5}
                        dataKey="commits"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {[
                          { name: 'XPV', commits: 67, color: THEME.accent.blue },
                          { name: 'Nexa', commits: 42, color: THEME.accent.green },
                          { name: 'Axiomatic', commits: 23, color: THEME.accent.purple },
                          { name: 'MCP', commits: 15, color: THEME.accent.yellow },
                        ].map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`${value} commits`, 'Count']} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </StatusCard>
            </div>
          </div>
        )}
        
        {/* Notion Tab */}
        {activeTab === 'notion' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <MetricsCard 
                title="Connected Workspaces" 
                value={notionStats.connectedWorkspaces} 
                icon={<Globe />} 
                color={THEME.accent.blue}
              />
              <MetricsCard 
                title="Active Databases" 
                value={notionStats.activeDatabases} 
                icon={<Database />} 
                color={THEME.accent.green}
              />
              <MetricsCard 
                title="Active Blocks" 
                value={notionStats.activeBlocks} 
                icon={<Code />} 
                color={THEME.accent.purple}
              />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <StatusCard title="Schema Versions" icon={<Database />}>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={[
                          { version: '3-1-0', databases: 8, color: THEME.accent.blue },
                          { version: '3-0-2', databases: 3, color: THEME.accent.green },
                          { version: '2-9-4', databases: 1, color: THEME.accent.yellow },
                        ]}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        fill="#8884d8"
                        paddingAngle={5}
                        dataKey="databases"
                        label={({ version, percent }) => `${version}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {[
                          { version: '3-1-0', databases: 8, color: THEME.accent.blue },
                          { version: '3-0-2', databases: 3, color: THEME.accent.green },
                          { version: '2-9-4', databases: 1, color: THEME.accent.yellow },
                        ].map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`${value} databases`, 'Count']} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </StatusCard>
              
              <StatusCard title="Recent Operations" icon={<Activity />}>
                <div className="space-y-0">
                  {[
                    { type: 'read', time: '10:42:18', target: 'Project Tracker', status: 'success' },
                    { type: 'update', time: '10:38:05', target: 'System Documentation', status: 'success' },
                    { type: 'create', time: '10:31:27', target: 'Meeting Notes', status: 'success' },
                    { type: 'delete', time: '10:22:55', target: 'Test Page', status: 'success' },
                    { type: 'update', time: '10:15:33', target: 'Component Library', status: 'error' },
                  ].map((operation, index, array) => (
                    <div 
                      key={`${operation.type}-${operation.time}`} 
                      className={`py-3 ${index < array.length - 1 ? 'border-b border-gray-100' : ''}`}
                    >
                      <div className="flex justify-between">
                        <div className="flex items-center">
                          <div 
                            className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                              operation.type === 'read' ? 'bg-blue-100 text-blue-600' : 
                              operation.type === 'update' ? 'bg-yellow-100 text-yellow-600' :
                              operation.type === 'create' ? 'bg-green-100 text-green-600' : 
                              'bg-red-100 text-red-600'
                            }`}
                          >
                            {operation.type === 'read' ? <Check size={16} /> : 
                             operation.type === 'update' ? <RefreshCw size={16} /> :
                             operation.type === 'create' ? <Check size={16} /> : 
                             <AlertCircle size={16} />}
                          </div>
                          <div>
                            <div className="flex items-center">
                              <span className="font-medium text-gray-800 capitalize">{operation.type}</span>
                              <span className="text-xs text-gray-500 ml-2">{operation.time}</span>
                            </div>
                            <p className="text-sm text-gray-700 mt-1">{operation.target}</p>
                          </div>
                        </div>
                        <div>
                          <span 
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              operation.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {operation.status}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </StatusCard>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Export the component
export default privDashboardPreview;

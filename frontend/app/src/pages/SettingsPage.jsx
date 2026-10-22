import { Card } from '../components/common/Card';
export function SettingsPage() {
    const securityControls = [
        'Argon2 password hashing',
        'HttpOnly session cookies',
        'SameSite protection',
        'CSRF tokens',
        'Tenant isolation',
        'Upload validation',
        'Rate limiting',
        'Audit events',
    ];
    const infrastructureServices = [
        'FastAPI /api/v1',
        'SQLAlchemy persistence',
        'Durable object storage',
        'WebSocket progress',
        'Passive analysis pipeline',
        'Report registry',
        'IOC registry',
        'Case linkage',
    ];
    return (<div className="grid2">
      <Card title="Security posture">
        <div className="settings-list">
          {securityControls.map((item) => (<div key={item}>
              <i /> {item}<span>enabled</span>
            </div>))}
        </div>
      </Card>
      <Card title="Infrastructure">
        <div className="settings-list">
          {infrastructureServices.map((item) => (<div key={item}>
              <i /> {item}<span>connected</span>
            </div>))}
        </div>
      </Card>
    </div>);
}

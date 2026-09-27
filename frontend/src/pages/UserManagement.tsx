import {
  useEffect,
  useState,
} from "react";

import {
  Users,
  Shield,
  User,
  RefreshCw,
} from "lucide-react";

import api from "../api/axios";

import {
  useAuth,
} from "../context/AuthContext";


interface UserData {
  id: number;
  name: string;
  email: string;
  department_id: number | null;
  role_id: number;
}


export default function UserManagement() {

  const {
    user,
  } = useAuth();

  const [
    users,
    setUsers,
  ] = useState<UserData[]>([]);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");


  async function loadUsers() {

    try {

      setLoading(true);
      setError("");

      const response =
        await api.get(
          "/api/v1/users"
        );

      setUsers(
        response.data
      );

    } catch (err) {

      console.error(
        "Users error:",
        err
      );

      setError(
        "Unable to load users."
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {

    if (
      user &&
      user.role_id === 1
    ) {
      loadUsers();
    }

  }, [user]);


  if (
    !user ||
    user.role_id !== 1
  ) {

    return (

      <div style={styles.page}>

        <div style={styles.denied}>

          <Shield size={45} />

          <h1>
            Access Restricted
          </h1>

          <p>
            User Management is available
            only to administrators.
          </p>

        </div>

      </div>
    );
  }


  return (

    <div style={styles.page}>

      <div style={styles.header}>

        <div>

          <h1 style={styles.title}>
            User Management
          </h1>

          <p style={styles.subtitle}>
            Manage organizational users
            and their access roles.
          </p>

        </div>

        <button
          onClick={loadUsers}
          style={styles.refreshButton}
        >
          <RefreshCw size={17} />
          Refresh
        </button>

      </div>


      {error && (

        <div style={styles.error}>
          {error}
        </div>

      )}


      <div style={styles.summary}>

        <Users size={25} />

        <div>

          <strong>
            {users.length}
          </strong>

          <span>
            Registered Users
          </span>

        </div>

      </div>


      <div style={styles.tableCard}>

        {loading ? (

          <div style={styles.loading}>
            Loading users...
          </div>

        ) : (

          <table style={styles.table}>

            <thead>

              <tr>

                <th style={styles.th}>
                  User
                </th>

                <th style={styles.th}>
                  Email
                </th>

                <th style={styles.th}>
                  Role
                </th>

                <th style={styles.th}>
                  Department
                </th>

              </tr>

            </thead>

            <tbody>

              {users.map(
                (item) => (

                  <tr key={item.id}>

                    <td style={styles.td}>

                      <div style={styles.userCell}>

                        <div style={styles.avatar}>
                          <User size={18} />
                        </div>

                        <div>
                          <strong style={styles.userName}>
                            {item.name}
                            </strong>

                            <span style={styles.userId}>
                            ID: {item.id}
                            </span>
                        </div>

                      </div>

                    </td>

                    <td style={styles.td}>
                      {item.email}
                    </td>

                    <td style={styles.td}>

                      <span style={styles.roleBadge}>
                        {getRoleName(
                          item.role_id
                        )}
                      </span>

                    </td>

                    <td style={styles.td}>

                      {item.department_id ??
                        "Not assigned"}

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        )}

      </div>

    </div>
  );
}


function getRoleName(
  roleId: number
) {

  if (roleId === 1) {
    return "Admin";
  }

  if (roleId === 2) {
    return "Manager";
  }

  return "Employee";
}


const styles: Record<
  string,
  React.CSSProperties
> = {

  page: {
    minHeight: "100vh",
    padding: "40px",
    background: "#f5f7fb",
    fontFamily:
      "Inter, Arial, sans-serif",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
  },

  title: {
    margin: 0,
    fontSize: "32px",
  },

  subtitle: {
    color: "#64748b",
  },

  refreshButton: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    padding: "11px 18px",
    border: "1px solid #cbd5e1",
    background: "#ffffff",
    borderRadius: "9px",
    cursor: "pointer",
  },

  summary: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    background: "#ffffff",
    border: "1px solid #e2e8f0",
    borderRadius: "15px",
    padding: "20px",
    width: "260px",
    marginBottom: "25px",
  },

  loading: {
    padding: "30px",
    textAlign: "center",
  },

  tableCard: {
    background: "#ffffff",
    border: "1px solid #e2e8f0",
    borderRadius: "16px",
    overflow: "hidden",
  },

  table: {
    width: "100%",
    borderCollapse: "collapse",
  },

  th: {
    textAlign: "left",
    padding: "16px",
    background: "#f8fafc",
    color: "#475569",
    fontSize: "14px",
  },

  td: {
    padding: "16px",
    borderTop: "1px solid #e2e8f0",
  },

  userCell: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
  },

  userName: {
  display: "block",
  fontWeight: 600,
  },

  userId: {
  display: "block",
  marginTop: "3px",
  fontSize: "12px",
  color: "#64748b",
  },

  avatar: {
    width: "38px",
    height: "38px",
    borderRadius: "50%",
    background: "#eff6ff",
    color: "#2563eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },

  roleBadge: {
    display: "inline-block",
    padding: "5px 10px",
    background: "#eff6ff",
    color: "#1d4ed8",
    borderRadius: "20px",
    fontSize: "13px",
    fontWeight: 600,
  },

  denied: {
    maxWidth: "500px",
    margin: "100px auto",
    textAlign: "center",
    background: "#ffffff",
    padding: "50px",
    borderRadius: "18px",
    border: "1px solid #e2e8f0",
  },

  error: {
    background: "#fee2e2",
    color: "#991b1b",
    padding: "15px",
    borderRadius: "10px",
    marginBottom: "20px",
  },
};
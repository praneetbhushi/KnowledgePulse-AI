import api from "./axios";

export const loginUser = async (
  username: string,
  password: string
) => {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);
  formData.append("grant_type", "password");

  const response = await api.post(
    "/api/v1/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  console.log("LOGIN RESPONSE:", response.data);

  return response.data;
};
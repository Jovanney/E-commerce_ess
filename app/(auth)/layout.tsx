import { FC, ReactNode } from "react";

interface AuthLayoutProps {
    children: ReactNode;
}

const AuthLayout: FC<AuthLayoutProps> = ({children}) => {
    return (
        <div className='p-10 rounded-md border-2 flex justify-center w-2/5 border-bluebord bg-azulforte'>
            {children}
        </div>
    ); 
};

export default AuthLayout;
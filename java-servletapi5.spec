%include	/usr/lib/rpm/macros.java
Summary:	Java servlet and JSP implementation classes
Name:		jakarta-servletapi5
Version:	5.5.23
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/tomcat/tomcat-5/v%{version}/src/apache-tomcat-%{version}-src.tar.gz
# Source0-md5:	cbf88ed51ee2be5a6ce3bace9d8bdb62
URL:		http://jakarta.apache.org/tomcat
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	rpm-javaprov
Provides:	jsp
Provides:	servlet
Provides:	servlet24
Provides:	servlet5
Provides:	servletapi5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This subproject contains the source code for the implementation
classes of the Java Servlet and JSP APIs (packages javax.servlet).

%package javadoc
Summary:	servletapi documentation
Summary(pl):	Dokumentacja do servletapi
Group:		Development/Languages/Java
Requires:	jpackage-utils

%description javadoc
servletapi documentation.

%description javadoc -l pl
Dokumentacja do servletapi.

%prep
%setup -q -n apache-tomcat-%{version}-src

%build
cd servletapi/jsr154
%ant dist \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

cd ../jsr152
%ant dist \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

%install
rm -rf $RPM_BUILD_ROOT
cd servletapi
install -d $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}/%{name}-%{version}}
install jsr152/dist/lib/jsp-api.jar $RPM_BUILD_ROOT%{_javadir}/jsp-api-%{version}.jar
install jsr154/dist/lib/servlet-api.jar $RPM_BUILD_ROOT%{_javadir}/servlet-api-%{version}.jar
ln -sf servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servlet.jar
ln -sf servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servletapi5.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr jsr152/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/jsp-api
cp -pr jsr154/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/servlet-api

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}

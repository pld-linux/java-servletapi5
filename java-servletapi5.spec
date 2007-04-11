%include	/usr/lib/rpm/macros.java
Summary:	Java servlet and JSP implementation classes
Summary(pl.UTF-8):	Klasy z implementacją Java Servlet i JSP
Name:		jakarta-servletapi5
Version:	5.5.23
Release:	1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/tomcat/tomcat-5/v%{version}/src/apache-tomcat-%{version}-src.tar.gz
# Source0-md5:	362d1d8b15dc09882440dcab8c592dd7
URL:		http://tomcat.apache.org/
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	rpm-javaprov
BuildRequires:	jdk >= 1.5
Provides:	jsp
Provides:	servlet
Provides:	servlet24
Provides:	servlet5
Provides:	servletapi5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This subproject contains the compiled code for the implementation
classes of the Java Servlet and JSP APIs (packages javax.servlet,
javax.servlet.http, javax.servlet.jsp, and javax.servlet.jsp.tagext).

%description -l pl.UTF-8
Ten podprojekt zawiera skompilowany kod implementacji klas API Java
Servlet i JSP (pakiety javax.servlet, javax.servlet.http,
javax.servlet.jsp i java.servlet.jsp.tagext).

%package javadoc
Summary:	servletapi documentation
Summary(pl.UTF-8):	Dokumentacja do servletapi
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
servletapi documentation.

%description javadoc -l pl.UTF-8
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

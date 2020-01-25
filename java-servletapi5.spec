# NOTE: for more recent version of servletapi see tomcat.spec
# TODO:
#   - fix all specs that requires servletapi5, servlet etc. They should require java(servlet)
#   - split into two packages, if it really needs to co-exist with other servlet-api.jar provider
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		jspapiver	2.0
%define		servletapiver	2.4


%define		srcname		servletapi5
Summary:	Java Servlet 2.4 and JSP 2.0 implementation classes
Summary(pl.UTF-8):	Klasy z implementacją Java Servlet 2.4 i JSP 2.0
Name:		java-servletapi5
Version:	5.5.33
Release:	1
License:	Apache v2
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/tomcat/tomcat-5/v%{version}/src/apache-tomcat-%{version}-src.tar.gz
# Source0-md5:	7811f4f1cdfd37cb22d421d2030818de
Patch0:		jakarta-servletapi5-target.patch
URL:		http://tomcat.apache.org/
BuildRequires:	ant
BuildRequires:	jdk >= 1.5
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
Requires:	jpackage-utils
Requires:	jre >= 1.5
Provides:	java(jsp) = %{jspapiver}
Provides:	java(servlet) = %{servletapiver}
Obsoletes:	classpathx_servlet
Obsoletes:	jakarta-servletapi
Obsoletes:	jakarta-servletapi5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This subproject contains the compiled code for the implementation
classes of the Java Servlet 2.4 and JSP 2.0 APIs (packages
javax.servlet, javax.servlet.http, javax.servlet.jsp, and
javax.servlet.jsp.tagext).

%description -l pl.UTF-8
Ten podprojekt zawiera skompilowany kod implementacji klas API Java
Servlet 2.4 i JSP 2.0 (pakiety javax.servlet, javax.servlet.http,
javax.servlet.jsp i java.servlet.jsp.tagext).

%package javadoc
Summary:	servletapi 5 documentation
Summary(pl.UTF-8):	Dokumentacja do servletapi 5
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	jakarta-servletapi5-javadoc

%description javadoc
servletapi 5 documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do servletapi 5.

%prep
%setup -qc
mv apache-tomcat-%{version}-src/servletapi/* .
%patch0 -p0

%build

%ant -f jsr154/build.xml dist \
	-Dbuild.compiler=extJavac \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

%ant -f jsr152/build.xml dist \
	-Dbuild.compiler=extJavac \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

%install
rm -rf $RPM_BUILD_ROOT

# JSP 2.0 and Servlet 2.4 classes
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a jsr152/dist/lib/jsp-api.jar $RPM_BUILD_ROOT%{_javadir}/jsp-api-%{jspapiver}.jar
cp -a jsr154/dist/lib/servlet-api.jar $RPM_BUILD_ROOT%{_javadir}/servlet-api-%{servletapiver}.jar

ln -s servlet-api-%{servletapiver}.jar $RPM_BUILD_ROOT%{_javadir}/servlet-api.jar
ln -s jsp-api-%{jspapiver}.jar $RPM_BUILD_ROOT%{_javadir}/jsp-api.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a jsr152/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}/jsp-api
cp -a jsr154/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}/servlet-api
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/jsp-api-%{jspapiver}.jar
%{_javadir}/jsp-api.jar
%{_javadir}/servlet-api-%{servletapiver}.jar
%{_javadir}/servlet-api.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
